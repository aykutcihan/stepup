# Post-mortem: return_comment Data Loss on Task Return

**Date:** 2026-05-15
**Branch:** `feature/fix-plan-flow-bugs`
**Severity:** Critical — silent data loss
**Outcome:** Column added to model + migration, schema updated, frontend renders feedback

---

## Initial State

The task return flow was implemented in `task_workflow_service.py`:

```python
async def return_task(self, db, task_id, current_user, data: ReturnTask):
    task = await self._get_task_for_manager(db, task_id, current_user)
    task.status = OnboardingPlanTaskStatus.IN_PROGRESS
    task.return_comment = data.content   # ← written here
    await db.commit()
```

The `ManagerTaskReviewPage` had a Return modal where the manager typed a comment. Submitting the form called this service method.

---

## The Bug

`task.return_comment = data.content` was written in the service but `return_comment` was never added to the `OnboardingPlanTask` model or the database schema.

**Outcome A — AttributeError (SQLAlchemy strict mode):** Setting an attribute that doesn't exist on a mapped class raises `AttributeError` at runtime.

**Outcome B — Silent loss (SQLAlchemy permissive mode):** The attribute is set on the Python object but SQLAlchemy does not include it in the `UPDATE` statement because it is not a mapped column. `await db.commit()` succeeds. No error is raised. The comment is gone.

Either way, the manager's feedback never reached the database. The employee saw the task returned to `IN_PROGRESS` with no explanation.

---

## Root Cause

The service code for `return_task` was written at the same time as the rest of the task workflow (US-015). The `return_comment` field was referenced in the service but the corresponding model column and Alembic migration were never created. The gap was not caught because:

1. The return flow path was not covered by integration tests that checked the database state after the operation
2. `return_comment` was also absent from `OnboardingPlanTaskResponse`, so the frontend had no way to display it even if it had been stored

---

## Discovery

Found during a cross-feature code review of the plan flow, when tracing the full return path from the manager's modal submit to the employee's plan page. Reading `task_workflow_service.py` and `onboarding_plan_task.py` side by side made the missing column obvious.

---

## Fix

**1. Model** (`app/models/onboarding_plan_task.py`):

```python
return_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
```

**2. Migration** (`alembic/versions/a1b2c3d4e5f6_add_return_comment_to_plan_tasks.py`):

```python
def upgrade() -> None:
    op.add_column(
        'onboarding_plan_tasks',
        sa.Column('return_comment', sa.Text, nullable=True),
    )
```

**3. Schema** (`app/schemas/onboarding_plan.py`):

```python
class OnboardingPlanTaskResponse(BaseModel):
    ...
    return_comment: str | None = None
```

**4. Frontend** (`EmployeePlanPage.tsx`) — renders the feedback box when `return_comment` is set:

```tsx
{task.return_comment && (
  <div className="bg-red-50 border border-red-200 rounded-lg px-3 py-2">
    <p className="text-xs font-medium text-red-700 mb-0.5">Manager feedback</p>
    <p className="text-xs text-red-600">{task.return_comment}</p>
  </div>
)}
```

---

## Lessons Learned

1. **Model, migration, and schema must be written together.** When a new field is referenced in service code, the model column, Alembic migration, and Pydantic response schema are all required. Missing any one of them silently breaks the feature.

2. **Silent SQLAlchemy behaviour is dangerous.** Setting an unmapped attribute on an ORM object does not raise an error — it is simply ignored by `db.commit()`. There is no warning. Tests that only check HTTP status codes or response shapes will not catch this.

3. **Test the full round-trip, not just the happy path status.** A test that calls `return_task` and checks the HTTP 200 response would pass even with this bug. The gap is only caught by a test that reads `return_comment` back from the database after the call.
