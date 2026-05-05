# StepUp

> Employee onboarding management platform

StepUp streamlines the process of onboarding new employees — structured task assignment, transparent progress tracking, and manager approval workflows, all in one place.

---

## Status

🚧 **In active development** — Sprint 1 complete, Sprint 2 (Auth) next

| Sprint | Theme | Status |
|---|---|---|
| Sprint 1 | Infrastructure | ✅ Complete |
| Sprint 2 | Authentication & Authorization | 🔄 BE Complete, FE Pending |
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

## Sprint 1 — What's Done

| US | Description |
|---|---|
| US-006 | Monorepo setup (Turborepo + pnpm) |
| US-007 | Docker + docker-compose local environment |
| US-008 | GCP project (Cloud Run, Cloud SQL, Secret Manager) |
| US-009 | GitHub Actions CI pipeline |
| US-010 | Database schema + Alembic initial migration |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic |
| **Database** | PostgreSQL 15 |
| **Frontend** | React 18, TypeScript, Tailwind CSS, shadcn/ui |
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
        core/         # Config, database connection
        models/       # SQLAlchemy models
      alembic/        # Database migrations
    frontend/         # React 18 + TypeScript application
      src/
        components/   # Reusable UI components
        pages/        # Route-based pages (hr/, manager/, employee/)
        hooks/        # Custom React hooks
        services/     # API call functions
        store/        # Zustand stores
        types/        # TypeScript types
        constants/    # Routes, API endpoints, error messages
  packages/
    shared-types/     # Shared TypeScript types
  docs/
    product-vision.md # Full product specification
    guides/           # Technical guides (Docker, Git, FastAPI, Alembic, etc.)
    adr/              # Architecture Decision Records
    scrum/            # Sprint planning and retrospectives
  docker-compose.yml
  turbo.json
```

---

## Local Development

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [pnpm](https://pnpm.io/installation)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/aykutcihan/stepup.git
cd stepup

# 2. Start the database
docker-compose up -d db

# 3. Run database migrations
docker-compose run --rm backend alembic upgrade head

# 4. Start all services
docker-compose up
```

### Services

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Frontend | http://localhost:3000 |
| Database | localhost:5433 |

> Port 5433 is used instead of the default 5432 (conflict with local PostgreSQL).

### Useful Commands

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

# Run all backend tests
docker exec stepup-backend python -m pytest --tb=short -q

# Run only unit tests
docker exec stepup-backend python -m pytest tests/unit --tb=short -q

# Run only integration tests
docker exec stepup-backend python -m pytest tests/integration --tb=short -q

# Start frontend (first time or after Dockerfile changes)
docker-compose up frontend --build

# Start frontend (subsequent runs)
docker-compose up frontend

# View frontend logs
docker-compose logs -f frontend

# Run frontend tests
docker-compose run --rm frontend node_modules/.bin/vitest run --config vitest.config.ts --passWithNoTests
```

---

## Documentation

| Document | Description |
|---|---|
| [`docs/product-vision.md`](./docs/product-vision.md) | Full product specification, user roles, workflows, architecture |
| [`docs/scrum/`](./docs/scrum/) | Sprint goals, refinement notes, reviews, retrospectives |
| [`docs/guides/`](./docs/guides/) | Technical guides (FastAPI, Docker, Git, Alembic, SQLAlchemy, etc.) |
| [`docs/adr/`](./docs/adr/) | Architecture Decision Records |

---

## Branch Strategy

```
main        → production (stable, merged at sprint end)
develop     → integration branch
feature/    → one branch per issue (feature/us-001-invite-user)
fix/        → bug fixes
test/be-    → backend tests for a user story (test/be-us-001-invitation-service)
test/fe-    → frontend tests for a user story (test/fe-us-001-invite-form)
```

All changes go through Pull Requests into `develop`.
`develop` is merged into `main` at the end of each sprint.