# Post-mortem: Backend Startup Failure After Schema-Service Import

**Date:** 2026-05-15
**Branch:** `feature/fix-plan-flow-bugs`
**Duration:** ~20 minutes
**Outcome:** Lazy import pattern adopted, backend running

---

## Initial State

As part of the plan flow bug fixes, `TaskAttachmentResponse` needed a `model_validator` that generates a `download_url` from the ORM object's `object_name`. The first implementation imported `StorageService` at the top of the schema file:

```python
# app/schemas/attachment.py — first attempt

from app.services.storage_service import StorageService

_storage = StorageService()

class TaskAttachmentResponse(BaseModel):
    ...
    @model_validator(mode='before')
    @classmethod
    def compute_download_url(cls, v):
        if isinstance(v, dict):
            return v
        return {
            ...
            'download_url': _storage.signed_url(v.object_name),
        }
```

`onboarding_plan.py` schema was also updated to import from `attachment.py`:

```python
# app/schemas/onboarding_plan.py
from app.schemas.attachment import TaskAttachmentResponse, TaskCommentResponse
```

---

## The Failure

After committing and starting the backend container:

```
File "/app/app/schemas/onboarding_plan.py", line 6, in <module>
    from app.schemas.attachment import TaskAttachmentResponse, TaskCommentResponse
  File "/app/app/schemas/attachment.py", line 4, in <module>
    from app.services.storage_service import StorageService
  File "/app/app/services/storage_service.py", line 3, in <module>
    from google.cloud import storage
ImportError: cannot import name 'storage' from 'google.cloud' (unknown location)
```

The backend refused to start. Login was unavailable.

---

## Diagnosis

### Issue 1 — Module-level import in schema layer

The import chain at startup:

```
router.py
  → onboarding_plan API
    → onboarding_plan schema
      → attachment schema          ← NEW: added by this PR
        → storage_service.py
          → google.cloud.storage   ← fails here
```

Before this change, `storage_service.py` was only imported via `attachment_service.py` → `attachments` API router. After the change, the same module was reached earlier through the schema layer. The underlying `google.cloud.storage` import was now triggered at startup before any request was made.

This revealed an architectural violation: **schema files should not import from the service layer**. Schemas define data shapes. Services contain infrastructure dependencies. Importing a service into a schema couples the data layer to the infrastructure layer and causes startup failures when the infrastructure is unavailable.

### Issue 2 — Stale Docker image

The `google.cloud.storage` import failure indicated the Docker image had a broken or outdated `google-cloud-storage` package installation. The package is in `requirements.txt` and was present on disk, but the running image had been built before a clean install was last performed.

Clearing Python `__pycache__` from the host and restarting the container did not help — the image itself needed to be rebuilt.

---

## Fix

**Part 1 — Lazy import inside the method body**

Moving the import inside the validator method means `google.cloud.storage` is only imported when the validator actually runs, not at module load time:

```python
# app/schemas/attachment.py — fixed

class TaskAttachmentResponse(BaseModel):
    ...
    @model_validator(mode='before')
    @classmethod
    def compute_download_url(cls, v):
        if isinstance(v, dict):
            return v
        from app.services.storage_service import StorageService   # ← lazy
        storage = StorageService()
        return {
            ...
            'download_url': storage.signed_url(v.object_name),
        }
```

Startup no longer touches `google.cloud.storage`. A GCS failure becomes a runtime error on the specific request that needs it, not a total startup failure.

**Part 2 — Docker image rebuild**

```powershell
docker compose build backend
docker compose up backend -d
```

Rebuilding ensured `google-cloud-storage` was freshly installed. After the rebuild the backend started cleanly.

---

## Lessons Learned

1. **Schemas must not import from services.** Schema files (`app/schemas/`) define data shapes for serialization. Service files (`app/services/`) contain business logic and infrastructure clients (GCS, SendGrid, etc.). Importing a service into a schema drags infrastructure dependencies into the startup path, causing failures unrelated to the request being served.

2. **Lazy imports isolate infrastructure from startup.** If a schema genuinely needs a service at serialization time (not at import time), import it inside the method body. Python caches modules — the first call imports it, subsequent calls reuse the cached module. There is no performance cost after the first invocation.

3. **Stale Docker images hide real failures.** The `google.cloud.storage` error existed in the running image before this PR. It was masked because the import was not triggered at startup in the old code. When the new import chain reached it earlier, the failure surfaced. A rebuild was required — not just a restart. When a backend fails to start with an import error for a package that is in `requirements.txt`, rebuild the image first before investigating the code.

4. **Test startup, not just functionality.** A backend that starts and a backend that serves requests are two different things. If import errors only surface at request time (e.g. lazy imports gone wrong), they will not be caught by unit tests. An integration test that starts the app and hits a health endpoint catches startup failures early.
