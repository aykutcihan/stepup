# ADR-009: Auth State Persistence via sessionStorage

**Date:** 2026-05-08
**Status:** Accepted

---

## Context

The frontend uses an in-memory Zustand store (`authStore`) to hold the authenticated user. On every full page load, the store resets to `{ user: null, isLoading: true }` and waits for a `GET /api/v1/auth/me` response before rendering protected content.

This caused two problems:

**1. Blank flash on page reload.**
Protected pages showed nothing (`null`) while `isLoading: true`, creating a visible loading gap before the route guard could evaluate the user's role.

**2. E2E RBAC test unreliable.**
The Playwright test navigates to `/hr/dashboard` via `page.goto()`, which triggers a full page reload. React mounts fresh, calls `getMe()` through the Vite proxy, and keeps `isLoading: true` until the request completes. In the Docker E2E environment, this request consistently took longer than the test assertion window (15 seconds), so `RequireRole` never got to evaluate the role and redirect to `/403`. The page stayed blank at `/hr/dashboard` despite the correct content eventually appearing.

---

## Decision

Persist the authenticated user object in `sessionStorage` and restore it synchronously on store initialization.

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
  isLoading: cachedUser === null,   // skip loading if user is cached
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

`getMe()` still runs in the background on every mount to verify the session is still valid. If it fails (expired token), `clearUser()` is called to remove the stale entry and let `RequireRole` redirect to `/login`.

---

## Alternatives Considered

**Keep in-memory only, fix proxy timing.**
The root cause of the E2E failure was the Vite proxy connection taking too long for the first request after a page reload. Adding an axios timeout (e.g. 5s) would make `getMe()` fail fast — but then `user` would be `null`, and `RequireRole` would redirect to `/login` instead of `/403`. The test expects `/403`, so this would not fix the test.

**Use localStorage.**
`localStorage` persists across browser sessions. For auth user data this is unnecessary and slightly riskier. `sessionStorage` is cleared when the tab closes, which is the expected lifetime.

**Use JWT in localStorage.**
Not applicable — auth tokens are stored in HttpOnly cookies (see ADR-004) and are never accessible to JavaScript.

---

## Consequences

**Gained:**
- No blank flash on page reload — `RequireRole` evaluates immediately with cached user.
- E2E RBAC test is deterministic — redirect to `/403` happens before `getMe()` returns.
- Logout correctly clears the cache via `clearUser()`.

**Trade-offs:**
- User metadata (`id`, `email`, `role`, `first_name`, `last_name`) is readable from JavaScript via `sessionStorage`. This is not a token exposure risk (tokens remain in HttpOnly cookies), but it is a consideration for XSS scenarios.
- Stale user data can briefly appear if the session expired between page loads. The background `getMe()` call corrects this within one request cycle.
