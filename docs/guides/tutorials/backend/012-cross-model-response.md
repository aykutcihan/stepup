# Cross-Model Response Construction

## The Problem

The standard response pattern is `ResponseSchema.model_validate(orm_instance)` — it works when all response fields map directly to a single ORM object. This breaks in two situations:

1. A response needs fields from **multiple related models** (e.g. task + plan + employee name)
2. A response needs a **computed field** that does not exist on the ORM object (e.g. a signed URL generated from `object_name`)

---

## Pattern 1 — Fields from Multiple Models

`ApprovalTaskResponse` combines fields from `OnboardingPlanTask`, `OnboardingPlan`, and `User` (the employee). There is no single ORM object to validate against.

**1. Define the schema without `from_attributes`**

```python
# app/schemas/onboarding_plan.py

class ApprovalTaskResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    title: str
    deadline: date
    status: OnboardingPlanTaskStatus
    employee_name: str          # from plan.employee
    plan_start_date: date       # from plan
    return_comment: str | None = None
    attachments: list[TaskAttachmentResponse] = []
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
                    return_comment=task.return_comment,
                    attachments=[
                        TaskAttachmentResponse.model_validate(a)
                        for a in task.attachments
                        if a.deleted_at is None
                    ],
                ))
    return result
```

`TaskAttachmentResponse.model_validate(a)` works here because `TaskAttachmentResponse` has a `model_validator` that handles ORM objects — see Pattern 2 below.

**3. Repository must eager-load all needed relationships**

```python
# app/repositories/onboarding_plan_repository.py

select(OnboardingPlan)
    .options(
        selectinload(OnboardingPlan.tasks).options(
            selectinload(OnboardingPlanTask.attachments),
            selectinload(OnboardingPlanTask.comments),
        ),
        selectinload(OnboardingPlan.employee),  # needed for employee_name
    )
```

---

## Pattern 2 — Computed Fields Not Present on the ORM

`TaskAttachmentResponse` needs a `download_url` field. This is a GCS signed URL generated at response time from `object_name`. The `TaskAttachment` ORM model has `object_name` but not `download_url`.

`model_validate(orm_obj)` with `from_attributes=True` reads attributes by name — it would fail because `download_url` is not an attribute on the model.

**Solution: `model_validator(mode='before')` with lazy import**

```python
# app/schemas/attachment.py

class TaskAttachmentResponse(BaseModel):
    id: uuid.UUID
    plan_task_id: uuid.UUID
    uploaded_by: uuid.UUID
    file_name: str
    file_type: str
    file_size: int
    download_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def compute_download_url(cls, v):
        if isinstance(v, dict):
            return v          # already built manually (e.g. in AttachmentService)
        from app.services.storage_service import StorageService
        storage = StorageService()
        return {
            'id': v.id,
            'plan_task_id': v.plan_task_id,
            'uploaded_by': v.uploaded_by,
            'file_name': v.file_name,
            'file_type': v.file_type,
            'file_size': v.file_size,
            'download_url': storage.signed_url(v.object_name),
            'created_at': v.created_at,
        }
```

The validator runs before Pydantic reads fields. When input is an ORM object (not a dict), it converts to dict and generates the signed URL inline. When input is already a dict (manual construction in `AttachmentService._to_response()`), it passes through unchanged.

The import of `StorageService` is inside the method body — **lazy import** — so `google.cloud.storage` is never imported at module load time. See `013-pydantic-model-validator.md` for why this matters.

---

## Rule

> Use `model_validate(orm_instance)` when the response maps to one ORM object and all fields exist as attributes.
> Build manually when the response aggregates fields from multiple objects.
> Use `model_validator(mode='before')` when a field must be computed at serialization time.

Manual construction is more verbose but avoids lazy-load errors and keeps the schema honest — it doesn't pretend to be an ORM-backed object when it isn't.
