# Cross-Model Response Construction

## The Problem

The standard response pattern is `ResponseSchema.model_validate(orm_instance)` — it works when all response fields map directly to a single ORM object. This breaks when a response needs fields from **multiple related models**.

`ApprovalTaskResponse` is an example: it combines fields from `OnboardingPlanTask`, `OnboardingPlan`, and `User` (the employee). There is no single ORM object to validate against.

---

## The Pattern

When a response spans multiple models, build it manually in the service layer.

**1. Define the schema without `from_attributes`**

```python
# app/schemas/onboarding_plan.py

class ApprovalTaskResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    title: str
    deadline: date
    status: OnboardingPlanTaskStatus
    employee_name: str       # from plan.employee
    plan_start_date: date    # from plan
    # no model_config — cannot use from_attributes here
```

**2. Build instances manually in the service**

```python
# app/services/task_workflow_service.py

async def get_pending_approvals(self, db, current_user):
    plans = await plan_repository.get_all_by_manager(db, current_user.id)
    result = []
    for plan in plans:
        for task in plan.tasks:
            if task.status == OnboardingPlanTaskStatus.COMPLETED:
                result.append(ApprovalTaskResponse(
                    id=task.id,
                    plan_id=task.plan_id,
                    title=task.title,
                    deadline=task.deadline,
                    status=task.status,
                    employee_name=f"{plan.employee.first_name} {plan.employee.last_name}",
                    plan_start_date=plan.start_date,
                    ...
                ))
    return result
```

**3. Repository must eager-load all needed relationships**

```python
# app/repositories/onboarding_plan_repository.py

select(OnboardingPlan)
    .options(
        selectinload(OnboardingPlan.tasks),
        selectinload(OnboardingPlan.employee),  # needed for employee_name
    )
```

---

## Rule

> Use `model_validate(orm_instance)` when the response maps to one ORM object.
> Build manually when the response aggregates fields from multiple objects.

Manual construction is more verbose but avoids lazy-load errors and keeps the schema honest — it doesn't pretend to be an ORM-backed object when it isn't.
