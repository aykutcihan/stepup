# API Organization

This guide defines how API routes are structured and organized in this project.

---

## Directory Structure

```
app/api/
    __init__.py
    router.py          ← aggregates all v1 routers, mounted in main.py
    v1/
        __init__.py
        auth.py        ← login, logout, refresh, register
        invitation.py  ← invitation management
        users.py       ← user management (added when needed)
        plans.py       ← onboarding plans (added when needed)
        tasks.py       ← task workflow (added when needed)
```

---

## router.py — The Aggregator

`main.py` knows only one thing: `api_router`. It does not know which endpoints exist.
All v1 routers are registered in `app/api/router.py`:

```python
# app/api/router.py
from fastapi import APIRouter
from app.api.v1 import auth, invitation

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(invitation.router, prefix="/invitations", tags=["invitations"])
```

`main.py` mounts it with the version prefix:

```python
# app/main.py
app.include_router(api_router, prefix="/api/v1")
```

**Why this pattern:** When a new domain is added (users, plans, tasks), only `router.py`
is updated — `main.py` never changes.

---

## One File Per Domain

Each file handles one domain — not one HTTP method, not one endpoint.

```
auth.py        → everything related to sessions (login, logout, refresh, register)
invitation.py  → everything related to invitations (create, list, resend, validate)
users.py       → everything related to users
```

**Why not put invite in auth.py?**
Invitation is an HR Admin operation — creating a resource. Authentication is session
management — login, logout, refresh. They have different actors, different
responsibilities, and will grow independently.

---

## Adding a New Domain

1. Create `app/api/v1/<domain>.py` with a `router = APIRouter()`
2. Add the router to `app/api/router.py`
3. Do not touch `main.py`

```python
# app/api/router.py
from app.api.v1 import auth, invitation, users  # add import

api_router.include_router(users.router, prefix="/users", tags=["users"])  # add line
```

---

## v1 as a Folder

`v1/` is a package, not just a URL prefix. This allows `v2/` to be added alongside it
when breaking changes are needed — both versions run simultaneously, old clients
are not affected. See ADR-006 for the full versioning decision.
