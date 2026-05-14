# State Machine Pattern

This guide explains how task status transitions are enforced in this project.

---

## The Problem

`OnboardingPlanTask` has a `status` field that can only move forward through a defined sequence. An employee must start a task before completing it. Arbitrary jumps (e.g. NOT_STARTED → COMPLETED) must return HTTP 400.

---

## Valid Transitions

```
NOT_STARTED  →  IN_PROGRESS   (start)
IN_PROGRESS  →  COMPLETED     (complete)
COMPLETED    →  APPROVED       (approve — manager, US-015)
COMPLETED    →  IN_PROGRESS   (return — manager, US-015)
```

CANCELLED and APPROVED are terminal — no further transitions allowed.

---

## Implementation

Transitions are expressed as a dict mapping the current status to the only valid next status:

```python
# app/services/task_workflow_service.py

VALID_TRANSITIONS = {
    OnboardingPlanTaskStatus.NOT_STARTED: OnboardingPlanTaskStatus.IN_PROGRESS,
    OnboardingPlanTaskStatus.IN_PROGRESS: OnboardingPlanTaskStatus.COMPLETED,
}
```

A single helper validates the transition before any mutation:

```python
def _assert_transition(
    self, task: OnboardingPlanTask, target: OnboardingPlanTaskStatus
) -> None:
    if VALID_TRANSITIONS.get(task.status) != target:
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

## Why a Dict Instead of if/elif

A dict makes the full transition table readable at a glance. Adding a new transition (e.g. RETURNED → IN_PROGRESS for manager return) is a one-line change with no branching logic to touch.

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

Before asserting the transition, the service verifies the task belongs to the authenticated user's active plan:

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

Returning `PLAN_TASK_NOT_FOUND` (not a 403) avoids leaking whether the task exists at all.
