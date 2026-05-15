# Pydantic model_validator — Computed Fields from ORM Objects

## The Problem

The standard pattern `ResponseSchema.model_validate(orm_obj)` reads field values from ORM attributes by name. This breaks when the response needs a field that does not exist on the ORM model — for example, a signed URL that must be generated at serialization time from a stored `object_name`.

```python
class TaskAttachmentResponse(BaseModel):
    download_url: str    # not an attribute on TaskAttachment ORM model
    ...

    model_config = ConfigDict(from_attributes=True)

# This fails — Pydantic cannot find 'download_url' on the ORM object
TaskAttachmentResponse.model_validate(attachment_orm_obj)
```

---

## The Solution — `model_validator(mode='before')`

A `model_validator(mode='before')` runs before Pydantic reads any fields. It receives the raw input — either a dict (when the schema is constructed manually) or an ORM object (when `model_validate` is called).

This is the right place to convert an ORM object to a dict and compute any derived fields:

```python
from pydantic import BaseModel, ConfigDict, model_validator

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
            return v          # already a dict — pass through unchanged
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

After this, both construction paths work:

```python
# Path 1: called from AttachmentService._to_response() — already a dict
TaskAttachmentResponse(id=..., download_url=signed_url, ...)

# Path 2: called from plan response — ORM object, URL computed by validator
TaskAttachmentResponse.model_validate(attachment_orm_obj)
```

---

## Lazy Import — Why the Import Is Inside the Method

The import of `StorageService` is inside the method body, not at the top of the file. This is intentional.

**The problem with a module-level import:**

```python
# attachment.py — schema file
from app.services.storage_service import StorageService  # ← module-level

_storage = StorageService()
```

When `attachment.py` is imported (which happens at startup, because `onboarding_plan.py` schema imports from it), Python immediately imports `storage_service.py`, which imports `google.cloud.storage`. If the GCS library has any issue — missing package, namespace conflict, environment not set up — the entire backend fails to start, even if no attachment is being served.

**With lazy import:**

```python
@model_validator(mode='before')
@classmethod
def compute_download_url(cls, v):
    if isinstance(v, dict):
        return v
    from app.services.storage_service import StorageService   # ← lazy
    storage = StorageService()
    ...
```

`google.cloud.storage` is only imported when the validator actually runs — that is, only when an attachment is being serialized. Startup succeeds regardless. A GCS failure becomes a runtime error on the specific request that needs it, not a total startup failure.

---

## Rule

> Schemas should be infrastructure-free at import time.
> If a schema needs a service (storage, email, etc.), import it lazily inside the method that uses it — never at module level.

This keeps the schema layer decoupled from infrastructure and prevents startup failures caused by unrelated service issues.

---

## When to Use This Pattern

Use `model_validator(mode='before')` when:

- A response field must be **computed** from another field on the ORM object (e.g. signed URL from `object_name`)
- The ORM field that drives the computation has a **different name** than the response field
- The computation requires calling a **service or external library**

Do not use it when `from_attributes=True` is sufficient — i.e. when all response fields exist as attributes on the ORM object with the same names.
