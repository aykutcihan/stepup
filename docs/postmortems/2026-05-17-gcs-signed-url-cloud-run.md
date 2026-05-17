# Post-mortem: GCS Signed URL Fails on Cloud Run (No Private Key)

**Date:** 2026-05-17
**Branch:** `feature/email-template-service`
**Severity:** High — `GET /api/v1/plans/me` 500 for any employee with attachments
**Outcome:** Storage service updated to use IAM-based signing; Cloud Run service account granted Token Creator role

---

## Initial State

`StorageService.signed_url()` generated GCS download URLs for task attachments:

```python
def signed_url(self, object_name: str, expiration_minutes: int = 60) -> str:
    blob = self._get_bucket().blob(object_name)
    return blob.generate_signed_url(
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
        version="v4",
    )
```

This worked locally because the developer's ADC (Application Default Credentials) pointed to a service account JSON key file, which contains a private key.

---

## The Bug

On Cloud Run, credentials are provided automatically by the GCP metadata server as `google.auth.compute_engine.credentials.Credentials`. These credentials contain only an **access token** — no private key.

`blob.generate_signed_url()` without explicit signing credentials attempts to sign the URL payload using the local private key. When no private key is available, it raises:

```
AttributeError: you need a private key to sign credentials.
the credentials you are currently using
<class 'google.auth.compute_engine.credentials.Credentials'>
just contains a token.
```

This exception was not caught. It propagated from inside a Pydantic `model_validator` → through `model_validate()` → unhandled → 500 Internal Server Error.

Any endpoint that serialized an `OnboardingPlanResponse` with attachments was affected.

---

## Root Cause

`generate_signed_url` has two signing modes:

| Mode | When used | Requirement |
|------|-----------|-------------|
| Local key signing | No explicit credentials passed | Private key in credentials |
| IAM signing | `service_account_email` + `access_token` passed | `iam.serviceAccounts.signBlob` permission |

The service always used local key signing. This worked in development (service account JSON key) but failed in production (Compute Engine token only).

---

## Fix

**1. Storage service — use IAM signing when running on Cloud Run:**

```python
# apps/backend/app/services/storage_service.py

import google.auth
import google.auth.transport.requests

def signed_url(self, object_name: str, expiration_minutes: int = 60) -> str:
    credentials, _ = google.auth.default()
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)  # also fetches service_account_email

    blob = self._get_bucket().blob(object_name)

    extra: dict = {}
    email = getattr(credentials, "service_account_email", None)
    token = getattr(credentials, "token", None)
    if email and email != "default" and token:
        extra["service_account_email"] = email
        extra["access_token"] = token

    return blob.generate_signed_url(
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
        version="v4",
        **extra,
    )
```

When `service_account_email` and `access_token` are passed, the GCS library delegates signing to the IAM API instead of using a local key. This works in both environments:
- **Local**: ADC returns a service account JSON key credential → `service_account_email` is set → IAM path taken (or falls back to key signing if `email` is absent)
- **Cloud Run**: Compute Engine credential → after `refresh()`, `service_account_email` contains the actual service account email → IAM path taken

**2. Grant IAM signing permission to the Cloud Run service account:**

```bash
gcloud projects add-iam-policy-binding stepup-494114 \
  --member="serviceAccount:943378472223-compute@developer.gserviceaccount.com" \
  --role="roles/iam.serviceAccountTokenCreator"
```

Without this role, the IAM signing API call would be rejected with a 403.

---

## Lessons Learned

1. **Test GCS signed URL generation in an environment without a service account key file.** The local ADC key masks this failure. Integration tests that run in CI (which uses Compute Engine credentials via Workload Identity or similar) would catch it.

2. **Always use IAM-based signing for production Cloud Run services.** Never rely on a local private key being present. The IAM signing pattern works in both local and production environments and requires only a role assignment rather than a key file.

3. **Errors inside Pydantic `model_validator` become opaque 500s.** The original traceback was buried under many middleware frames. When a `model_validator` calls external services (like storage), any exception from that service will be an unhandled 500. Consider wrapping external calls in the validator with explicit error handling.
