# Post-mortem: Trailing Slash 307 Redirect Blocks Invitation API

**Date:** 2026-05-17
**Branch:** `feature/email-template-service`
**Severity:** High — invitation create and list completely broken in production
**Outcome:** Added trailing slash to two frontend API endpoint constants

---

## Initial State

The invitation form allowed HR admins to send onboarding invitations. The backend routes were:

```python
@router.post("/")   # POST /api/v1/invitations/
@router.get("/")    # GET  /api/v1/invitations/
```

The frontend called:

```ts
// apiEndpoints.ts
INVITATIONS: {
  CREATE: '/api/v1/invitations',   // ← no trailing slash
  LIST:   '/api/v1/invitations',   // ← no trailing slash
}
```

---

## The Bug

FastAPI has `redirect_slashes=True` by default. When a request arrives at `/api/v1/invitations` (no trailing slash), FastAPI returns a **307 Temporary Redirect** pointing to `/api/v1/invitations/`.

On Cloud Run, the redirect `Location` header was set to `http://...run.app/api/v1/invitations/` (HTTP, not HTTPS). The browser, loading the app from an HTTPS Firebase Hosting origin, blocked the follow-up request due to **mixed content policy** — HTTPS pages cannot make HTTP requests. The request never reached the backend.

**Symptoms observed:**
- Invite form showed "Something went wrong. Please try again." immediately after submit
- "Pending Invitations" always empty (GET also 307'd)
- Network tab showed `Status Code: 307 Temporary Redirect` with `Location: http://...`

---

## Root Cause

Inconsistency between the FastAPI route definition (trailing slash required) and the frontend endpoint constant (no trailing slash). All other endpoint groups in `apiEndpoints.ts` already had trailing slashes. The invitation endpoints were added without following the same convention.

---

## Fix

```ts
// apps/frontend/src/constants/apiEndpoints.ts
INVITATIONS: {
  CREATE: '/api/v1/invitations/',  // added /
  LIST:   '/api/v1/invitations/',  // added /
}
```

---

## Lessons Learned

1. **All FastAPI `"/"` routes need a trailing slash on the client.** When a FastAPI route is defined as `@router.post("/")`, the full path ends with `/`. Calling it without the trailing slash triggers a redirect. On Cloud Run behind a Google Frontend proxy, this redirect degrades from HTTPS to HTTP, which browsers block.

2. **Follow the trailing slash convention consistently.** Every other endpoint group in this project uses trailing slashes (`/api/v1/users/`, `/api/v1/departments/`). The invitation endpoints were added without following the pattern. A linting rule or code review checklist item would catch this.

3. **307 redirects in cross-origin HTTPS → HTTP scenarios are silent failures.** The frontend shows a generic error and the network tab is the only place to see the 307. Always check the Network tab before assuming the backend has a bug.
