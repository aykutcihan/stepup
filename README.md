# StepUp

> Employee onboarding management platform

StepUp streamlines the process of onboarding new employees — structured task assignment, transparent progress tracking, and manager approval workflows, all in one place.

---

## Status

🚧 **In active development** — Sprint 1 in progress

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic |
| **Database** | PostgreSQL 15 |
| **Frontend** | React 18, TypeScript, Tailwind CSS, shadcn/ui |
| **Infrastructure** | Docker, GCP Cloud Run, GCP Cloud SQL |
| **CI/CD** | GitHub Actions |
| **Package Manager** | pnpm (monorepo with Turborepo) |

---

## Project Structure

```
stepup/
  apps/
    backend/          # FastAPI application
    frontend/         # React application
  packages/
    shared-types/     # Shared TypeScript types
  docs/
    product-vision.md # Full product specification
    setup-log.md      # Development log
    guides/           # Learning notes and technical guides
    adr/              # Architecture Decision Records
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
```

---

## Documentation

Full technical documentation is in the [`docs/`](./docs/) folder:

| Document | Description |
|---|---|
| [`product-vision.md`](./docs/product-vision.md) | Full product specification, user roles, workflows, architecture |
| [`setup-log.md`](./docs/setup-log.md) | Day-by-day development log |
| [`guides/`](./docs/guides/) | Technical guides (FastAPI, Docker, Alembic, etc.) |
| [`adr/`](./docs/adr/) | Architecture Decision Records |

---

## GitHub Projects

Sprint progress is tracked on the [StepUp Board](https://github.com/users/aykutcihan/projects/5).

---

## Contributing

This is a solo learning project. Branch strategy:

```
main      → production (stable)
develop   → integration branch
feature/  → one branch per issue
fix/      → bug fixes
```

All changes go through Pull Requests into `develop`.
`develop` is merged into `main` at the end of each sprint.