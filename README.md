# StepUp

> Employee onboarding management platform

StepUp streamlines the process of onboarding new employees — structured task assignment, transparent progress tracking, and manager approval workflows, all in one place.

---

## Status

| Sprint | Theme | Status |
|---|---|---|
| Sprint 1 | Infrastructure | ✅ Complete |
| Sprint 2 | Authentication & Authorization | ✅ Complete |
| Sprint 3 | User & Department Management | — |
| Sprint 4 | Onboarding Template Management | — |
| Sprint 5 | Onboarding Plan & Task Workflow | — |
| Sprint 6 | Notifications & Email | — |
| Sprint 7 | Dashboards | — |
| Sprint 8 | Attachments | — |
| Sprint 9 | Audit Trail & Reports | — |
| Sprint 10 | Quality & Polish | — |

Sprint progress is tracked on the [StepUp Board](https://github.com/users/aykutcihan/projects/5).

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic |
| **Database** | PostgreSQL 15 |
| **Frontend** | React 18, TypeScript, Tailwind CSS |
| **Infrastructure** | Docker, GCP Cloud Run, GCP Cloud SQL, GCP Secret Manager |
| **CI/CD** | GitHub Actions |
| **Package Manager** | pnpm (monorepo with Turborepo) |

---

## Project Structure

```
stepup/
  apps/
    backend/          # FastAPI application
      app/
        api/          # Route handlers
        core/         # Config, database, limiter
        models/       # SQLAlchemy models
        services/     # Business logic
        repositories/ # Database queries
        schemas/      # Pydantic schemas
      alembic/        # Database migrations
      scripts/        # Seed and utility scripts
      tests/          # Unit and integration tests
    frontend/         # React 18 + TypeScript application
      src/
        app/          # App entry, routing
        components/   # Shared UI components
        constants/    # Routes, API endpoints, messages
        features/     # Feature-based modules (auth, invitation, users)
        lib/          # API client
        stores/       # Zustand stores
        types/        # Generated API types
      tests/
        e2e/          # Playwright E2E tests
  docs/
    adr/              # Architecture Decision Records
    postmortems/      # Debug and incident records
    guides/           # Technical guides
    scrum/            # Sprint planning and retrospectives
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
# 1. Clone the repository
git clone https://github.com/aykutcihan/stepup.git
cd stepup

# 2. Install frontend dependencies
pnpm install

# 3. Create frontend env file
echo "VITE_API_URL=" > apps/frontend/.env

# 4. Run database migrations
docker-compose run --rm backend alembic upgrade head

# 5. Seed the database with test users
docker-compose run --rm backend python scripts/seed.py
```

### Running the app

There are two ways to run the app locally. The hybrid approach is recommended for active frontend development.

#### Option A — Hybrid (recommended for FE development)

Backend and database run in Docker. Frontend runs locally for instant hot reload.

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
| Database | localhost:5433 |

#### Option B — Full Docker

Everything runs in Docker containers.

```bash
docker-compose up db backend frontend
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Database | localhost:5433 |

> Port 5433 is used instead of the default 5432 to avoid conflicts with a locally installed PostgreSQL.

### Test users

After running the seed script, the following users are available:

| Email | Password | Role |
|---|---|---|
| admin@stepup.com | Admin1234! | HR Admin |
| manager@stepup.com | Manager1234! | Manager |
| employee@stepup.com | Employee1234! | Employee |

---

## E2E Tests

Two modes are available depending on the context.

### Docker (CI / pre-push)

Runs in an isolated container — same environment as CI. Slower due to Vite cold start (~5 min for full suite).

```bash
# Run migrations and seed (once, or after DB reset)
docker-compose run --rm backend alembic upgrade head

# Run all E2E tests
docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"

# Run a specific test file
docker-compose run --rm playwright sh -c "pnpm install && pnpm exec playwright test tests/e2e/login.spec.ts"
```

The `seeder` service runs automatically as part of the Playwright dependency chain — no manual seed step needed.

### Local (during development)

Runs against the local Vite dev server. Much faster (~1-2 min) since Vite is already warm.

**Prerequisites:** backend running (`docker-compose up db backend`) and frontend running (`pnpm --filter frontend dev`).

```bash
# First-time setup: install browser binary
pnpm --filter frontend exec playwright install chromium

# Run all E2E tests locally
pnpm --filter frontend e2e:local

# Run a specific test file
pnpm --filter frontend exec playwright test --config apps/frontend/playwright.config.local.ts tests/e2e/login.spec.ts
```

| | Docker | Local |
|---|---|---|
| Speed | ~5 min | ~1-2 min |
| Workers | 1 | 2 |
| Test timeout | 120s | 30s |
| Use when | CI, pre-push | Active development |

---

## Useful Commands

```bash
# Run database migrations
docker-compose run --rm backend alembic upgrade head

# Seed the database
docker-compose run --rm backend python scripts/seed.py

# Create a new migration after model changes
docker-compose run --rm backend alembic revision --autogenerate -m "description"

# Access the database directly
docker exec -it stepup-db psql -U stepup -d stepup_db

# View backend logs
docker-compose logs -f backend

# Rebuild backend image (after requirements.txt changes)
docker-compose build backend

# Run backend tests
docker-compose run --rm backend pytest --tb=short -q

# Run frontend unit tests
pnpm --filter frontend test
```

---

## Documentation

| Document | Description |
|---|---|
| [`docs/product-vision.md`](./docs/product-vision.md) | Full product specification, user roles, workflows |
| [`docs/adr/`](./docs/adr/) | Architecture Decision Records |
| [`docs/postmortems/`](./docs/postmortems/) | Debug and incident records |
| [`docs/guides/`](./docs/guides/) | Technical guides (FastAPI, Docker, Git, Alembic, etc.) |
| [`docs/scrum/`](./docs/scrum/) | Sprint goals, refinement notes, reviews, retrospectives |

---

## Branch Strategy

```
main           → production (stable, merged at sprint end)
develop        → integration branch
feature/be-    → backend feature work  (feature/be-us-004-department)
feature/fe-    → frontend feature work (feature/fe-us-004-department)
fix/           → bug fixes
test/be-       → backend tests  (test/be-us-001-invitation-service)
test/fe-       → frontend tests (test/fe-us-001-invite-form)
```

BE and FE are developed on separate branches per user story, allowing independent PRs and reviews.

All changes go through Pull Requests into `develop`.
`develop` is merged into `main` at the end of each sprint.
