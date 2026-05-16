# Post-mortem: Production Login Failure Due to Stale Migration Job Image

**Date:** 2026-05-16
**Severity:** Critical — full production outage, no user could log in
**Outcome:** Deploy workflow fixed to update migration-job image before execution

---

## Initial State

Production was working. The CI/CD pipeline in `deploy-production.yml` deployed backend images to Cloud Run and executed `migration-job` to run Alembic migrations. The `migration-job` Cloud Run Job had been created manually once during initial GCP setup.

---

## The Bug

The deploy workflow executed `migration-job` but never updated its container image:

```yaml
# Before fix — only executes, never updates the job's image
- name: Run database migrations
  run: |
    gcloud run jobs execute migration-job \
      --region ${{ env.REGION }} \
      --project ${{ env.PROJECT_ID }} \
      --wait
```

`migration-job` is a Cloud Run Job with a fixed container image. It only knows about Alembic migrations that existed at the time its image was last set. When new migrations were added and the backend was redeployed with a newer image, `migration-job` still ran with the old image — meaning `alembic upgrade head` did nothing, because the new migration files did not exist in the old image.

The backend code referenced `users.avatar_url` and `invitations.department_id` (added by migrations `f1a2b3c4d5e6` and `14e90742db5f`), but those columns were never created in the production database. Every query on the `users` or `invitations` tables raised:

```
asyncpg.exceptions.UndefinedColumnError: column users.avatar_url does not exist
```

---

## Blast Radius

- `POST /api/v1/auth/login` → 500 (queries `users` table)
- `GET /api/v1/invitations/validate` → 500 (queries `invitations` table)
- All other authenticated endpoints → 500 (all use `users` via `get_current_user`)
- **Result:** No user could log in. The entire production application was non-functional.

---

## Discovery

Browser showed "Something went wrong. Please try again." on the login page. Diagnosis path:

1. Health endpoint `/health` returned 200 — backend was running
2. CORS preflight returned correct `Access-Control-Allow-Origin` — not a CORS issue
3. `POST /api/v1/auth/login` with valid credentials → 500
4. `POST /api/v1/auth/login` with invalid email format → 422 (Pydantic worked fine)
5. Cloud Run logs showed `UndefinedColumnError: column users.avatar_url does not exist`
6. Compared `migration-job` image SHA vs backend service image SHA — they were different

---

## Fix

**Immediate:** Updated the migration-job image manually and re-ran it:

```bash
gcloud run jobs update migration-job \
  --image europe-west4-docker.pkg.dev/stepup-494114/cloud-run-source-deploy/stepup/stepup-backend:77eba8ba \
  --region europe-west4 --project stepup-494114

gcloud run jobs execute migration-job \
  --region europe-west4 --project stepup-494114 --wait
```

**Permanent:** Updated `deploy-production.yml` to always update the job image before executing:

```yaml
- name: Update migration job image
  run: |
    gcloud run jobs update migration-job \
      --image ${{ env.IMAGE }}:${{ github.sha }} \
      --region ${{ env.REGION }} \
      --project ${{ env.PROJECT_ID }}

- name: Run database migrations
  run: |
    gcloud run jobs execute migration-job \
      --region ${{ env.REGION }} \
      --project ${{ env.PROJECT_ID }} \
      --wait
```

---

## Lessons Learned

1. **Cloud Run Jobs do not auto-update their image.** Unlike a Cloud Run Service (which gets a new image on each deploy), a Cloud Run Job keeps whatever image it was last configured with. Executing a job re-runs the old image unless you explicitly update it first.

2. **A successful job execution (exit code 0) does not mean migrations ran.** `alembic upgrade head` exits 0 when there is nothing to do — including when the migration files simply do not exist in the container. The job appeared green in GCP Console but had applied nothing.

3. **Deploy and migrate must use the same image.** The backend service and the migration job must always run identical code. Any divergence creates a window where the schema and the ORM models are out of sync.

4. **Diagnose with the logs, not the frontend error.** "Something went wrong" on the login page could mean dozens of things. The actual error (`UndefinedColumnError`) was visible immediately in Cloud Run logs via `gcloud run services logs read`.
