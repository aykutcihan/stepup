# GitHub Actions — CI Pipeline

This guide covers the CI pipeline configuration for the StepUp project.

---

## Triggers

The pipeline runs on:
- Push to `develop` or `main`
- Pull request targeting `develop` or `main`

---

## Jobs

### test-backend

Runs backend tests in a clean Ubuntu environment with a real PostgreSQL database.

#### PostgreSQL Service

Integration tests require a real database. The pipeline spins up a PostgreSQL 15 container as a service:

```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: stepup
      POSTGRES_PASSWORD: stepup123
      POSTGRES_DB: stepup_test
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

The `options` block makes the job wait until PostgreSQL is ready before running tests — without this, the DB might not be accepting connections yet.

#### Environment Variables

All variables required by `pydantic-settings` must be provided. Missing required variables cause the app to fail at import time, even in tests.

```yaml
env:
  DATABASE_URL: postgresql+asyncpg://stepup:stepup123@localhost:5432/stepup_test
  TEST_DATABASE_URL: postgresql+asyncpg://stepup:stepup123@localhost:5432/stepup_test
  FRONTEND_URL: http://localhost:3000
  SENDGRID_API_KEY: ci-placeholder
  SENDGRID_FROM_EMAIL: noreply@stepup.local
  JWT_SECRET_KEY: ci-test-secret-key
```

Note: `DATABASE_URL` and `TEST_DATABASE_URL` both point to `stepup_test` in CI — there is only one database in this environment.

#### Dependencies

Install from `requirements.txt`, not just `pytest`. The full dependency list includes `pytest-asyncio`, `httpx`, `sqlalchemy`, `asyncpg`, and others required at import time.

```yaml
- name: Install dependencies
  run: |
    pip install --upgrade pip
    pip install -r requirements.txt
```

#### Running Tests

```yaml
- name: Run tests
  run: |
    if [ -d "tests" ] && [ "$(ls -A tests)" ]; then
      python -m pytest --tb=short -q
    else
      echo "No tests found, skipping..."
    fi
```

`python -m pytest` is used instead of bare `pytest` to ensure the correct Python environment is used.

The `if` check skips the step if no test files exist yet — prevents the job from failing on branches without tests.

---

### test-frontend

Runs frontend tests using pnpm. No database required.

---

## Common Failures

### `ModuleNotFoundError: No module named 'pytest_asyncio'`

**Cause:** Only `pytest` was installed, not the full `requirements.txt`.

**Fix:** Change `pip install pytest` to `pip install -r requirements.txt` in the workflow.

### Tests fail with missing env var

**Cause:** `pydantic-settings` raises a validation error if a required variable is missing. This happens at import time, before any test runs.

**Fix:** Add the missing variable to the `env` block in the workflow.
