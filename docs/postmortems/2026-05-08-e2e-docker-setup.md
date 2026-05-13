# Post-mortem: E2E Docker Infrastructure Setup and Test Stability

**Date:** 2026-05-08
**Branch:** `test/fe-e2e-sprint-2`
**Duration:** ~1 day
**Outcome:** 7/7 tests passing

---

## Initial State

Playwright E2E tests were written as part of Sprint 2, covering the following scenarios:

- HR Admin, Manager, Employee login → redirect to the correct dashboard
- Wrong password → stay on login page
- Employee attempting to access `/hr/dashboard` → redirect to `/403`
- Deactivated user sees error message on login page
- Invalid invitation token shows error message on registration page

Running `docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"` resulted in **all 7 tests failing**.

At the same time, the local development environment had become noticeably slow — API requests were taking much longer than expected.

---

## Issue 1 — Local development environment was slow

### Symptom

`localhost:3000` responded slowly. Pages loaded but API calls had a visible delay on every request.

### Root Cause

A change had been made to `apiClient.ts`:

```ts
// Before
baseURL: import.meta.env.VITE_API_URL,

// After (incorrect change)
baseURL: '',
```

With `baseURL: ''`, all API requests were going through the Vite dev server proxy instead of directly to the backend. This extra network hop added latency to every request.

The Vite proxy had been added to `vite.config.ts` to enable Docker E2E networking. The proxy is necessary in Docker but adds unnecessary overhead in local development.

### Fix

`apiClient.ts` was updated to:

```ts
baseURL: import.meta.env.VITE_API_URL || '',
```

`docker-compose.yml` was updated to set `VITE_API_URL: ""` for the frontend service:

```yaml
frontend:
  environment:
    VITE_API_URL: ""
```

The logic works as follows:
- **Local:** `.env` provides `VITE_API_URL=http://localhost:8000` → connects directly to backend, no proxy, fast.
- **Docker:** `VITE_API_URL=""` is set as an OS env var, overriding the `.env` file → `baseURL: ''` → proxy routes requests to `http://backend:8000`.

`.env.example` was also updated (`BACKEND_URL` → `VITE_API_URL=http://localhost:8000`).

---

## Issue 2 — Frontend healthcheck made the container unhealthy

### Symptom

Running `docker-compose run --rm playwright` caused the frontend container to hang in `Waiting` state, then fail:

```
dependency failed to start: container stepup-frontend is unhealthy
```

### Root Cause

The initial healthcheck used an HTTP request:

```yaml
test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000', r => process.exit(0)).on('error', () => process.exit(1))"]
interval: 5s
timeout: 10s
```

When Vite starts, it performs on-demand dependency pre-bundling. During this phase it listens on port 3000 but cannot respond to HTTP requests within 10 seconds. Every healthcheck timed out, causing the container to be marked unhealthy.

### Fix

Replaced the HTTP check with a TCP port check:

```yaml
healthcheck:
  test: ["CMD", "node", "-e", "require('net').createConnection({host:'localhost',port:3000},()=>process.exit(0)).on('error',()=>process.exit(1))"]
  interval: 5s
  timeout: 5s
  retries: 12
  start_period: 60s
```

The TCP check does not wait for Vite to produce an HTTP response. It passes as soon as the port is open, which happens immediately when the Vite process starts. `start_period: 60s` gives extra time for slow volume mount initialization on Windows/Docker Desktop.

The playwright `depends_on` was updated:

```yaml
playwright:
  depends_on:
    frontend:
      condition: service_healthy
    backend:
      condition: service_started
```

---

## Issue 3 — Playwright container started but all tests timed out: Vite "Blocked request"

### Symptom

After fixing the healthcheck, tests started running. All login tests timed out at 30–60 seconds:

```
Error: page.fill: Test timeout of 60000ms exceeded.
Call log:
  - waiting for locator('input[placeholder="Email"]')
```

`page.goto('/login')` appeared to succeed, but the form never appeared.

### Diagnosis

The `error-context.md` file inside `test-results/` was read. Playwright automatically generates this file for every failing test and includes a page snapshot:

```yaml
- generic [ref=e2]: "Blocked request. This host (\"frontend\") is not allowed.
  To allow this host, add \"frontend\" to server.allowedHosts in vite.config.js."
```

The page was completely blank. React had never mounted. Vite 5 rejects requests from non-localhost hostnames by default as a security measure against DNS rebinding attacks.

Playwright connects using `baseURL: 'http://frontend:3000'`, where `frontend` is the Docker service name. Vite did not recognize this as an allowed host.

### Fix

One line added to `vite.config.ts`:

```ts
server: {
  allowedHosts: ['frontend'],
  ...
}
```

The frontend container was restarted after this change (a running container does not pick up config changes automatically).

**Note:** This issue was diagnosed in under 5 minutes by reading the error-context.md page snapshot. Without it, the failure would likely have been misattributed to Vite cold start, proxy configuration, or React mounting issues — each of which would have taken much longer to investigate.

---

## Issue 4 — Seeder container "exit 1"

### Symptom

The `seeder` service was introduced to automatically seed test users before the playwright container starts. It exited with code 1:

```
service "seeder" didn't complete successfully: exit 1
```

### Root Cause

`seed.py` imported the application config at the top level:

```python
from app.core.config import settings
engine = create_async_engine(settings.DATABASE_URL)
```

The `Settings` model (`pydantic_settings.BaseSettings`) declares these fields as required:

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_URL: str          # required
    SENDGRID_API_KEY: str      # required
    SENDGRID_FROM_EMAIL: str   # required
    JWT_SECRET_KEY: str        # required
```

The seeder container was only given `DATABASE_URL`. The `ValidationError` was raised at import time, causing the Python process to exit 1 before running any seed logic.

Additionally, the seeder service had no volume mount, so the updated `seed.py` on disk was not reflected in the container. The container ran the version baked into the image at build time.

### Fix

The `settings` dependency was removed from `seed.py`:

```python
# Before
from app.core.config import settings
engine = create_async_engine(settings.DATABASE_URL)

# After
import os
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_async_engine(DATABASE_URL)
```

A volume mount was added to the seeder service in `docker-compose.yml`:

```yaml
seeder:
  volumes:
    - ./apps/backend:/app
```

`seed.py` was already written to be idempotent — if a user exists it skips, if not it creates. This makes it safe to run on every E2E invocation.

---

## Issue 5 — Login endpoint rate limit caused test failures

### Symptom

Backend logs showed `429 Too Many Requests` during some test runs. The login endpoint was protected with `@limiter.limit("5/minute")`. The full E2E suite performs 5+ login attempts, all from the same Docker network IP, hitting the limit.

### Fix

The rate limit was made configurable via an environment variable:

```python
# limiter.py
LOGIN_RATE_LIMIT = os.getenv("LOGIN_RATE_LIMIT", "5/minute")

# auth.py
@limiter.limit(LOGIN_RATE_LIMIT)
async def login(...):
```

`docker-compose.yml` backend service:

```yaml
environment:
  LOGIN_RATE_LIMIT: "1000/minute"
```

Production behavior is preserved (default `5/minute`). The Docker dev environment is not rate-limited during E2E runs.

---

## Issue 6 — HR dashboard triggered a 307 Temporary Redirect on every load

### Symptom

Backend logs showed:

```
GET /api/v1/users → 307 Temporary Redirect → GET /api/v1/users/
```

An extra round-trip on every user list request.

### Root Cause

The backend route was defined with a trailing slash:

```python
@router.get("/")  # serves at /api/v1/users/
```

The frontend called it without one:

```ts
LIST: '/api/v1/users',  // causes 307
```

### Fix

One character change in `apiEndpoints.ts`:

```ts
LIST: '/api/v1/users/',
```

---

## Issue 7 — RBAC test: URL stayed at `/hr/dashboard` for 60 seconds

This was the most complex issue. It involved multiple overlapping causes and took the longest to diagnose correctly.

### Test Scenario

```ts
test('Employee accessing HR dashboard is redirected to 403', async ({ page }) => {
  await login(page, 'employee@stepup.com', 'Employee1234!')
  await page.waitForURL('**/employee/dashboard')

  await page.goto('/hr/dashboard')
  await expect(page).toHaveURL('/403')
})
```

### Symptom

The test timed out at 60 seconds every run. `toHaveURL('/403')` was retried for 15 seconds and always received `/hr/dashboard`.

### False Trails

Four different code-level approaches were attempted to fix this:

1. Added `useEffect + navigate` inside `RequireRole` → no effect
2. Added page-level role checks inside each dashboard component → no effect
3. Rewrote `RequireRole` to wrap children directly instead of using `<Outlet>` → no effect
4. Added a global path-based guard `useEffect` inside `App.tsx` → no effect

The fact that none of these worked was itself an important signal: the problem was not in the application logic.

### Diagnosis — Layer 1: Was the page rendering at all?

The `error-context.md` file was read after the latest test run:

```yaml
- heading "403 — You do not have permission to access this page." [level=1]
```

**The 403 page was rendering.** The redirect was working. But the URL was still `/hr/dashboard` and the test was timing out.

### Diagnosis — Layer 2: Timing

Test durations were examined:

| Test | Duration |
|------|----------|
| HR Admin login | 55.1s |
| Manager login | 40.7s |
| Employee login | 41.4s |
| Wrong password | 21.1s |
| **RBAC (timeout)** | **60s** |

The RBAC test logs in as employee — this takes ~41 seconds based on the Employee login test. After that, `page.goto('/hr/dashboard')` and `expect(toHaveURL('/403'))` need to fit in the remaining time. With a 60-second test timeout, there was not enough room.

The redirect was working correctly. The test was simply running out of time.

### Diagnosis — Layer 3: Why does login take 40 seconds?

`page.goto('/hr/dashboard')` is a full page navigation. React mounts fresh. `App.tsx` calls `getMe()` in a `useEffect`. This request goes through the Vite proxy.

Two compounding factors:

**Factor A — Vite cold compile:**
On the first several requests, Vite compiles JavaScript modules on demand. This takes 20–40 seconds for the first test runs in a session.

**Factor B — Proxy connection reuse issue:**
When `page.goto('/hr/dashboard')` fires a full page navigation, any pending request from the previous page (the `getMe()` called when the previous React app was mounted) is cancelled by the browser. The Vite proxy sometimes leaves the corresponding backend connection in an inconsistent state. When the new page's `getMe()` request arrives, the proxy attempts to reuse this stale connection. The request hangs indefinitely. `isLoading` never becomes `false`. `RequireRole` returns `null`. The URL stays at `/hr/dashboard`.

This explains why all four code-level fix attempts failed: the guard code was correct, but the state it depended on (`isLoading: false`) was never reached because `getMe()` never resolved.

### Fix — Two Parts

**Part 1: sessionStorage persistence in authStore**

The authenticated user is now persisted to `sessionStorage` and restored synchronously on store initialization:

```ts
const STORAGE_KEY = 'auth_user'

function loadUser(): User | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as User) : null
  } catch {
    return null
  }
}

const cachedUser = loadUser()

export const useAuthStore = create<AuthStore>((set) => ({
  user: cachedUser,
  isLoading: cachedUser === null,  // skip loading state if user is cached
  setUser: (user) => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(user))
    set({ user })
  },
  clearUser: () => {
    sessionStorage.removeItem(STORAGE_KEY)
    set({ user: null })
  },
  setLoading: (isLoading) => set({ isLoading }),
}))
```

After employee login, `setUser` saves to sessionStorage. When `page.goto('/hr/dashboard')` triggers a full page reload:

1. React mounts fresh
2. `loadUser()` reads the employee from sessionStorage synchronously
3. Store starts with `{ user: employee, isLoading: false }`
4. `RequireRole` evaluates immediately: employee + HR_ADMIN required → `<Navigate to="/403" />`
5. Redirect happens before `getMe()` returns

`getMe()` still runs in the background to verify the session. If verification fails (expired token), `clearUser()` removes the stale cache and the user is redirected to login.

**Part 2: Test timeout increase**

```ts
// playwright.config.ts
timeout: 120000,  // 60s → 120s
```

The Vite dev server in Docker genuinely takes 40–55 seconds for the first few test runs due to on-demand module compilation. 120 seconds accommodates the full login flow with room for the subsequent navigation and assertion.

---

## Minor Findings

### Playwright config was missing key settings

```ts
// Before
export default defineConfig({
  testDir: './tests/e2e',
  use: { baseURL: 'http://frontend:3000' },
})

// After
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 120000,
  expect: { timeout: 15000 },
  workers: 1,
  use: { baseURL: 'http://frontend:3000' },
})
```

`workers: 1` is important: three parallel workers hitting Vite simultaneously tripled the cold compile load. With serial execution, the first test triggers compilation and all subsequent tests benefit from the warm cache.

### Login helper needed an explicit visibility wait

```ts
// Before
await page.goto('/login')
await page.fill('input[placeholder="Email"]', email)

// After
await page.goto('/login', { waitUntil: 'domcontentloaded' })
await expect(page.getByPlaceholder('Email')).toBeVisible()
await page.fill('input[placeholder="Email"]', email)
```

`domcontentloaded` lets `goto` return earlier. The explicit `toBeVisible()` wait (using `expect.timeout: 15000`) ensures React has mounted and the form is ready before interaction.

### Dashboard components had redundant role checks

While attempting to fix the RBAC test, role check logic was added directly inside `HRDashboard`, `ManagerDashboard`, and `EmployeeDashboard`. This duplicated what `RequireRole` already handles and risked triggering double navigation. These additions were removed after the tests passed.

---

## Summary

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Slow local dev | `baseURL: ''` → all requests through proxy | Context-aware baseURL via `VITE_API_URL` env var |
| Frontend unhealthy | HTTP healthcheck timed out during Vite pre-bundling | TCP port healthcheck (`net.createConnection`) |
| Playwright "Blocked request" | Vite 5 blocks non-localhost hostnames | `allowedHosts: ['frontend']` |
| Seeder exit 1 | `Settings` import required env vars not provided to seeder | Read `DATABASE_URL` directly from `os.environ` |
| Rate limit 429 | 5/min limit hit by E2E suite from same IP | `LOGIN_RATE_LIMIT` env var, set to `1000/minute` in Docker |
| 307 redirect | Frontend missing trailing slash on users endpoint | `'/api/v1/users/'` |
| RBAC test timeout | No sessionStorage → `getMe()` hung → `isLoading: true` → no redirect | sessionStorage persistence + timeout increase |

**Final result: 7/7 tests passing ✓**

---

## Lessons Learned

1. **Read the error context file first.** Playwright generates a `test-results/.../error-context.md` with a page snapshot for every failing test. Reading this before making any code changes would have saved hours on Issues 3 and 7.

2. **Distinguish "logic is wrong" from "logic never runs".** Four guard implementations failed on the RBAC test because the state the guards depended on (`isLoading: false`) was never reached. The symptom (URL unchanged) looked like a routing bug but was actually a timing/networking issue one layer below.

3. **Docker networking resolves in layers.** Container started ≠ service ready. Service ready ≠ application ready. Each layer needs its own readiness strategy.

4. **Shared config models create hidden dependencies.** Standalone scripts like `seed.py` should not load the full application config. They should declare only the env vars they actually need.

5. **Test timing failures are deceptive.** "URL did not change" and "page did not render" look identical in a Playwright timeout but have completely different root causes. A page snapshot is the fastest way to tell them apart.
