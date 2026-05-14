# StepUp

> Employee onboarding management platform

StepUp replaces email chains and spreadsheets with a structured onboarding workflow — task assignment, progress tracking, manager approvals, file uploads, automated reminders, and analytics in one place.

---

## Live Demo

| | URL |
|---|---|
| **Frontend** | https://stepup-494114.web.app |
| **Backend API** | https://stepup-backend-943378472223.europe-west4.run.app/docs |

**Demo credentials:**

| Role | Email | Password |
|---|---|---|
| HR Admin | admin@stepup.com | Admin1234! |
| Manager (Engineering) | manager@stepup.com | Manager1234! |
| Manager (Product) | manager2@stepup.com | Manager1234! |
| Employee (Engineering, in progress) | employee@stepup.com | Employee1234! |
| Employee (Engineering, completed) | alice@stepup.com | Employee1234! |
| Employee (Product, stuck) | bob@stepup.com | Employee1234! |

---

## Features

### HR Admin
- Invite users by email with role and department pre-assigned
- Manage departments and user accounts (deactivate, reactivate)
- Create and manage onboarding templates per department (tasks, deadlines, required/optional)
- Clone templates between departments
- Create onboarding plans for employees from active templates
- Adjust plans after creation (deadlines, cancel tasks, add tasks)
- Role-based dashboard with org-wide stats
- Audit trail — full history of all system actions, filterable
- Reports — avg completion time by department, task rates by template, bottleneck analysis — all exportable to CSV

### Manager
- Dashboard with team onboarding status and pending approval count
- Review completed tasks — approve or return with mandatory feedback
- Notifications when employees complete tasks

### Employee
- View assigned onboarding plan and task list
- Start and complete tasks (state machine enforced)
- Upload files per task (PDF, DOCX, PNG, JPEG — max 10 MB) stored in GCP Cloud Storage
- Add comments to tasks
- View manager feedback on returned tasks
- Notifications on plan start, task approved/returned, deadline reminders

### System (automated)
- APScheduler marks tasks as Overdue daily when deadline passes
- Deadline reminder emails sent 2 days before due date
- Overdue tasks remain actionable — employee and manager notified

---

## Status

| Sprint | Theme | Status |
|---|---|---|
| Sprint 1 | Infrastructure & CI/CD | ✅ Complete |
| Sprint 2 | Authentication & Authorization | ✅ Complete |
| Sprint 3 | User & Department Management | ✅ Complete |
| Sprint 4 | Onboarding Template Management | ✅ Complete |
| Sprint 5 | Plan Creation & Task Workflow | ✅ Complete |
| Sprint 6 | Manager Review & UI Polish | ✅ Complete |
| Sprint 7 | Role-Based Dashboards & Audit Trail | ✅ Complete |
| Sprint 8 | Email Notifications | ✅ Complete |
| Sprint 9 | Scheduler, Reports, File Upload & Seed | ✅ Complete |
| Sprint 10 | Quality & Polish (US-021) | 🔶 In Progress |

Sprint progress is tracked on the [StepUp Board](https://github.com/users/aykutcihan/projects/5).

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0 (async), Alembic |
| **Database** | PostgreSQL 15 |
| **Auth** | JWT (HttpOnly cookies), bcrypt, refresh token rotation |
| **Email** | SendGrid |
| **File Storage** | GCP Cloud Storage (signed URLs) |
| **Scheduler** | APScheduler (runs inside FastAPI lifespan) |
| **Rate Limiting** | slowapi |
| **Frontend** | React 18, TypeScript, Tailwind CSS, Zustand, Axios |
| **Testing (BE)** | pytest, httpx (unit + integration) |
| **Testing (FE)** | Vitest, React Testing Library |
| **Testing (E2E)** | Playwright |
| **Infrastructure** | Docker, GCP Cloud Run, GCP Cloud SQL, GCP Cloud Storage, GCP Secret Manager |
| **CI/CD** | GitHub Actions |
| **Monorepo** | Turborepo + pnpm |

---

## Project Structure

```
stepup/
  apps/
    backend/          # FastAPI application
      app/
        api/          # Route handlers (v1/)
        core/         # Config, database, dependencies, limiter
        enums/        # Shared enum types
        errors/       # Exception classes, messages, handlers
        models/       # SQLAlchemy models
        repositories/ # Database queries
        schemas/      # Pydantic request/response schemas
        services/     # Business logic
      alembic/        # Database migrations
      scripts/        # Seed script
      tests/
        unit/         # Unit tests (services)
        integration/  # API endpoint tests
    frontend/         # React 18 + TypeScript
      src/
        app/          # App entry, routing
        components/   # Shared UI components
        constants/    # Routes, API endpoints, error codes, roles
        features/     # Feature modules (auth, plan, template, audit, reports…)
        layouts/      # Dashboard layouts per role
        lib/          # Axios client + interceptor
        stores/       # Zustand auth store
        types/        # api.ts (OpenAPI-aligned type definitions)
      tests/e2e/      # Playwright E2E tests
  docs/
    adr/              # Architecture Decision Records
    guides/           # Technical guides (FastAPI, Alembic, Docker, testing…)
    postmortems/      # Debug and incident records
    scrum/            # Sprint goals, reviews, retrospectives
  docker-compose.yml
  turbo.json
```

---

## Local Development

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 18+](https://nodejs.org/)
- [pnpm](https://pnpm.io/installation)

### First-time setup

```bash
# 1. Install frontend dependencies
pnpm install

# 2. Create frontend env file
echo "VITE_API_URL=" > apps/frontend/.env

# 3. Build Docker images
docker-compose build

# 4. Run database migrations
docker-compose run --rm backend alembic upgrade head

# 5. Seed the database
docker-compose run --rm seeder
```

> **File upload (optional):** To test file upload locally, place a GCP service account key at `gcs-key.json` in the project root and set `GCS_BUCKET_NAME` in `.env`. Without this, the app works fully except for the file upload feature.

### Scenario 1 — Full Docker

Everything runs in Docker.

```bash
docker-compose up db backend frontend
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Database | localhost:5433 |

### Scenario 2 — Frontend Local

Database and backend in Docker, frontend runs locally for faster hot reload.

**Terminal 1:**
```bash
docker-compose up db backend
```

**Terminal 2:**
```bash
pnpm --filter frontend dev
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

> Port 5433 is used instead of 5432 to avoid conflicts with a locally installed PostgreSQL.

### Seed data

The seeder creates a realistic dataset covering all task states and features:

| User | Role | Department | Plan state |
|---|---|---|---|
| admin@stepup.com | HR Admin | Human Resources | — |
| manager@stepup.com | Manager | Engineering | — |
| manager2@stepup.com | Manager | Product | — |
| employee@stepup.com | Employee | Engineering | In progress (mix of statuses) |
| alice@stepup.com | Employee | Engineering | Completed (all approved) |
| bob@stepup.com | Employee | Product | Stuck (returned + overdue tasks) |

---

## Running Tests

### Backend

```bash
# Unit tests
docker-compose run --rm backend pytest tests/unit/ -v

# Integration tests (requires running db)
docker-compose run --rm backend pytest tests/integration/ -v

# All tests
docker-compose run --rm backend pytest --tb=short -q
```

### Frontend

```bash
# Unit + component tests
pnpm --filter frontend test

# Watch mode
pnpm --filter frontend test:watch
```

### E2E (Playwright)

```bash
# Docker (CI / pre-push) — full isolated run
docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"

# Local (faster, requires Scenario 2 running)
pnpm --filter frontend exec playwright install chromium   # first time only
pnpm --filter frontend e2e:local
```

| | Docker | Local |
|---|---|---|
| Speed | ~5 min | ~1-2 min |
| Use when | CI, pre-push | Active development |

---

## Useful Commands

```bash
# Run database migrations
docker-compose run --rm backend alembic upgrade head

# Create a new migration after model changes
docker-compose run --rm backend alembic revision --autogenerate -m "description"

# Access the database directly
docker exec -it stepup-db psql -U stepup -d stepup_db

# View backend logs
docker-compose logs -f backend

# Rebuild backend image (after requirements.txt changes)
docker-compose build backend

# Run frontend unit tests
pnpm --filter frontend test
```

---

## Documentation

| Document | Description |
|---|---|
| [`docs/product-vision.md`](./docs/product-vision.md) | Product specification, user roles, workflow, roadmap |
| [`docs/adr/`](./docs/adr/) | Architecture Decision Records |
| [`docs/guides/`](./docs/guides/) | Technical guides (FastAPI, Alembic, Docker, testing, conventions) |
| [`docs/scrum/`](./docs/scrum/) | Sprint goals, reviews, retrospectives |
| [`docs/postmortems/`](./docs/postmortems/) | Debug and incident records |

---

## Branch Strategy

```
main       → production (stable, merged at sprint end)
develop    → integration branch (all PRs target this)
feature/   → feature work  (feature/us-020-admin-reports)
fix/       → bug fixes
```

All changes go through Pull Requests into `develop`.  
`develop` is merged into `main` at the end of each sprint.
