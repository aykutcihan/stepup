# FastAPI Route Registration Order

## The Problem

FastAPI matches routes in the order they are registered. When a parameterized route like `GET /plans/{plan_id}` is registered before a literal route like `GET /plans/me`, Starlette matches `GET /plans/me` against `{plan_id}` first. FastAPI then runs the dependency chain (including `require_role`) before validating that `"me"` is a valid UUID — which means the wrong auth check fires and the caller gets a 403 instead of reaching the intended endpoint.

**Example that causes the bug:**

```python
# router.py — wrong order
api_router.include_router(onboarding_plan.router, prefix="/plans")  # has GET /{plan_id}
api_router.include_router(task_workflow.plans_router, prefix="/plans")  # has GET /me
```

`GET /api/v1/plans/me` hits `GET /plans/{plan_id}` (HR_ADMIN) → 403 for an employee.

---

## The Fix

Register the router with the more specific (literal) path **before** the router with the parameterized path:

```python
# router.py — correct order
api_router.include_router(task_workflow.plans_router, prefix="/plans")  # GET /me first
api_router.include_router(onboarding_plan.router, prefix="/plans")      # GET /{plan_id} after
```

---

## Rule

> Whenever two routers share the same prefix and one has a literal path that would be shadowed by a path parameter in the other, register the literal-path router first.

---

## How This Was Caught

Integration test `test_returns_200_with_tasks` returned 403 instead of 200. The employee client was correctly set up, but the wrong endpoint was matched. Swapping the include order fixed it.
