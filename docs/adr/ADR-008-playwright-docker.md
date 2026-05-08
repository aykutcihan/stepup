# ADR-008: Playwright E2E Tests in a Dedicated Docker Container

**Date:** 2026-05-07
**Status:** Accepted

---

## Context

Sprint 2 requires E2E tests covering login, registration, and role-based routing. Playwright needs browser binaries (Chromium, Firefox, WebKit) and their system-level dependencies to run.

The frontend runs in a `node:18-slim` Docker container. Two options were considered for running Playwright tests in the local Docker environment.

---

## Decision

We run Playwright tests in a **dedicated Docker service** using the official `mcr.microsoft.com/playwright` image, added to `docker-compose.yml`.

### Service chain

```
db → backend → frontend (healthy) → playwright
                    ↑
              seeder (completed)
```

- `frontend` must pass a TCP healthcheck on port 3000 before `playwright` starts.
- `seeder` runs seed users into the database and must exit 0 before `playwright` starts.
- `playwright` depends on both with `condition: service_healthy` / `condition: service_completed_successfully`.

### docker-compose.yml (relevant services)

```yaml
frontend:
  healthcheck:
    test: ["CMD", "node", "-e", "require('net').createConnection({host:'localhost',port:3000},()=>process.exit(0)).on('error',()=>process.exit(1))"]
    interval: 5s
    timeout: 5s
    retries: 12
    start_period: 60s

seeder:
  build:
    context: ./apps/backend
    dockerfile: Dockerfile
  command: ["python", "scripts/seed.py"]
  environment:
    DATABASE_URL: ${DATABASE_URL}
  volumes:
    - ./apps/backend:/app
  depends_on:
    - db
    - backend

playwright:
  build:
    context: .
    dockerfile: apps/frontend/Dockerfile.e2e
  volumes:
    - ./apps/frontend:/app
  working_dir: /app
  user: root
  depends_on:
    frontend:
      condition: service_healthy
    backend:
      condition: service_started
    seeder:
      condition: service_completed_successfully
```

`Dockerfile.e2e` extends the official Playwright image with pnpm:
```dockerfile
FROM mcr.microsoft.com/playwright:v1.59.1-noble
RUN npm install -g pnpm@10
```

### Playwright config

`playwright.config.ts` is configured for the Docker network environment:

```ts
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 120000,
  expect: { timeout: 15000 },
  workers: 1,
  use: {
    baseURL: 'http://frontend:3000',
  },
})
```

- `baseURL` uses the Docker service hostname `frontend`, not `localhost`.
- `workers: 1` prevents parallel requests from overwhelming the Vite dev server's cold compilation.
- `timeout: 120000` accounts for the full login flow through the Vite proxy.

### Vite configuration requirements

`vite.config.ts` requires two additions for Docker E2E to work:

```ts
server: {
  allowedHosts: ['frontend'],   // Vite 5 blocks non-localhost hostnames by default
  proxy: {
    '/api': {
      target: process.env.BACKEND_URL || 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

`allowedHosts` is required because the Playwright browser accesses Vite via the `frontend` Docker hostname. Without it, Vite returns a blank "Blocked request" page.

The proxy lets the browser call `/api/*` on the same origin (`frontend:3000`) and have Vite forward to the backend container — avoiding cross-origin issues with cookies.

### API client configuration

`apiClient.ts` uses an empty `baseURL` in Docker so requests go through the Vite proxy:

```ts
baseURL: import.meta.env.VITE_API_URL || '',
```

`docker-compose.yml` sets `VITE_API_URL: ""` for the frontend service to override the local `.env` value (`http://localhost:8000`). Locally, the `.env` value is used directly for better performance.

### Run procedure

**Prerequisites (run once, or after DB reset):**
```powershell
docker-compose run --rm backend alembic upgrade head
```

**Run E2E tests:**
```powershell
docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"
```

The `seeder` service runs automatically as part of the dependency chain — no manual seed step required.

---

## Alternatives Considered

**Install Playwright inside the frontend container (`node:18-slim`)**

`node:18-slim` is a minimal image with no browser dependencies. Installing Playwright inside it requires adding dozens of system packages (`libglib2.0-0`, `libnss3`, `libatk1.0-0`, and many more). This bloats the image, increases build time, and makes the Dockerfile harder to maintain.

---

## Consequences

**Gained:**
- Frontend container stays clean — no browser dependencies or Playwright binaries
- Official Playwright image has all browser dependencies pre-installed and versioned
- Seed users are created automatically before tests run
- Frontend healthcheck ensures Vite is serving before Playwright starts
- Same pattern as backend tests: `docker-compose run --rm backend pytest` → `docker-compose run --rm playwright pnpm e2e`

**Trade-offs:**
- One additional service in `docker-compose.yml`
- First run pulls the Playwright image (~1.5GB) — one-time cost
- Vite dev server (not a production build) is used for E2E — first test run is slower due to on-demand module compilation
