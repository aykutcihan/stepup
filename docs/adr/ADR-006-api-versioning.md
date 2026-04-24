# ADR-006: API Versioning with /api/v1/ Prefix

**Date:** 2026-04-21
**Status:** Accepted

---

## Context

StepUp's React frontend communicates with the FastAPI backend via a RESTful API. As the product evolves, breaking changes to the API may be needed. Without versioning, any breaking change forces the frontend and backend to be deployed simultaneously, increasing deployment risk and making it impossible to support multiple clients on different versions.

---

## Decision

All API endpoints are prefixed with `/api/v1/`.

```
/api/v1/auth/login
/api/v1/users/
/api/v1/plans/
/api/v1/tasks/
```

A central router mounts all v1 routes:

```python
# app/api/router.py
router.include_router(auth.router, prefix="/api/v1/auth")
router.include_router(users.router, prefix="/api/v1/users")
```

---

## Alternatives Considered

**No versioning**
Simplest approach — no prefix, routes like `/auth/login`. However, this makes introducing breaking changes later impossible without coordinating simultaneous deploys of frontend and backend. Ruled out.

**Header-based versioning**
Clients send an `Accept: application/vnd.stepup.v1+json` header. This is RESTfully correct but harder to test in a browser, less visible in logs, and less intuitive for a portfolio project. URL-based versioning is more common in practice.

**Subdomain versioning**
Routing via `v1.api.stepup.com`. Requires DNS and infrastructure changes per version — overkill for this project.

---

## Consequences

**Gained:**
- Future breaking changes can be introduced as `/api/v2/` routes without breaking existing clients
- Versioning is visible in every request URL — easy to trace in logs
- No extra configuration needed — FastAPI's `include_router` with a prefix handles it cleanly
- Industry-standard pattern that employers recognize immediately

**Trade-offs:**
- Slightly longer URLs
- When v2 is introduced, shared logic between v1 and v2 routes needs careful management to avoid duplication