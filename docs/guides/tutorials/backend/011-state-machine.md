# State Machine Pattern

This guide explains how task status transitions are enforced in this project.

---

## The Problem

`OnboardingPlanTask` has a `status` field that can only move forward through a defined sequence. An employee must start a task before completing it. Arbitrary jumps (e.g. NOT_STARTED → COMPLETED) must return HTTP 400.

---

## Valid Transitions

```
NOT_STARTED  →  IN_PROGRESS              (employee: start)
IN_PROGRESS  →  COMPLETED               (employee: complete)
OVERDUE      →  IN_PROGRESS             (employee: start — task missed deadline but not yet started)
OVERDUE      →  COMPLETED               (employee: complete — task was in progress when deadline passed)
COMPLETED    →  APPROVED                (manager: approve)
COMPLETED    →  IN_PROGRESS             (manager: return — sends back for rework)
```

CANCELLED and APPROVED are terminal — no further transitions allowed.

---

## Implementation

Transitions are expressed as a dict mapping each status to the **set** of valid next statuses:

```python
# app/services/task_workflow_service.py

VALID_TRANSITIONS: dict[OnboardingPlanTaskStatus, set[OnboardingPlanTaskStatus]] = {
    OnboardingPlanTaskStatus.NOT_STARTED: {OnboardingPlanTaskStatus.IN_PROGRESS},
    OnboardingPlanTaskStatus.IN_PROGRESS: {OnboardingPlanTaskStatus.COMPLETED},
    OnboardingPlanTaskStatus.OVERDUE: {
        OnboardingPlanTaskStatus.IN_PROGRESS,
        OnboardingPlanTaskStatus.COMPLETED,
    },
}
```

A single helper validates the transition before any mutation:

```python
def _assert_transition(
    self, task: OnboardingPlanTask, target: OnboardingPlanTaskStatus
) -> None:
    if target not in VALID_TRANSITIONS.get(task.status, set()):
        raise ValidationError(*messages.INVALID_TASK_TRANSITION)
```

Each action method calls `_assert_transition` before updating the status:

```python
async def start_task(self, db, task_id, current_user):
    task = await self._get_task_for_user(db, task_id, current_user)
    self._assert_transition(task, OnboardingPlanTaskStatus.IN_PROGRESS)
    task.status = OnboardingPlanTaskStatus.IN_PROGRESS
    await db.commit()
    await db.refresh(task)
    return task
```

---

## Why a Set Instead of a Single Value

The first version of `VALID_TRANSITIONS` mapped each status to a single next status (a plain value, not a set). This broke when `OVERDUE` was introduced — an overdue task can transition to either `IN_PROGRESS` or `COMPLETED` depending on context. A set makes this explicit and keeps `_assert_transition` a one-liner (`target not in ...`) with no branching.

Adding a new transition is a one-line change to the dict. No branching logic needs to change.

---

## OVERDUE Status

The scheduler (`apscheduler`) runs nightly and transitions any `NOT_STARTED` or `IN_PROGRESS` task whose deadline has passed to `OVERDUE`. Once overdue, the task is still actionable — the employee can start it (→ `IN_PROGRESS`) or mark it complete directly (→ `COMPLETED`).

---

## return_comment

When a manager returns a task, the task transitions `COMPLETED → IN_PROGRESS` and the return comment is stored on the task:

```python
async def return_task(self, db, task_id, current_user, data: ReturnTask):
    task = await self._get_task_for_manager(db, task_id, current_user)
    ...
    task.status = OnboardingPlanTaskStatus.IN_PROGRESS
    task.return_comment = data.content   # stored on the task, shown to employee
    await db.commit()
```

The `return_comment` column is nullable — it is only set when the task has been returned at least once. The employee sees this feedback in their plan page.

---

## Error Response

Invalid transitions return HTTP 400:

```json
{
  "success": false,
  "error_code": "INVALID_TASK_TRANSITION",
  "message": "This task cannot transition from its current status"
}
```

---

## Ownership Check

Before asserting the transition, the service verifies the task belongs to the right actor.

**Employee actions** — task must belong to the employee's active plan:

```python
async def _get_task_for_user(self, db, task_id, current_user):
    task = await plan_task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
    plan = await plan_repository.get_active_by_user(db, current_user.id)
    if not plan or task.plan_id != plan.id:
        raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
    return task
```

**Manager actions** — task must belong to a plan the manager owns:

```python
async def _get_task_for_manager(self, db, task_id, current_user):
    task = await plan_task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
    plan = await plan_repository.get_by_id(db, task.plan_id)
    if not plan or plan.manager_id != current_user.id:
        raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)
    return task
```

Both return `PLAN_TASK_NOT_FOUND` (not a 403) to avoid leaking whether the task exists at all.
