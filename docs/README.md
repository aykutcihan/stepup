# Documentation

All project documentation lives here. Each folder has a distinct purpose.

---

## Structure

| Folder / File | Purpose |
|---------------|---------|
| [`product-vision.md`](product-vision.md) | Full product specification — user roles, features, workflows, architecture decisions |
| [`adr/`](adr/) | Architecture Decision Records — why specific technical choices were made |
| [`scrum/`](scrum/) | Sprint planning, refinement notes, reviews, and retrospectives |
| [`guides/`](guides/) | Technical guides — conventions, tooling, infrastructure, tutorials |

---

## adr/

Architecture Decision Records. Each file documents one decision: the context, the options considered, and why we chose what we chose.

| File | Decision |
|------|----------|
| `ADR-001` | FastAPI as backend framework |
| `ADR-002` | GCP stack (Cloud Run, Cloud SQL, Secret Manager) |
| `ADR-003` | State management approach |
| `ADR-004` | HttpOnly cookies for auth tokens |
| `ADR-005` | Monorepo with Turborepo |
| `ADR-006` | API versioning strategy |
| `ADR-007` | Structured logging |

---

## scrum/

Sprint artifacts — what was planned, what was built, what was learned.

| Folder | Contains |
|--------|----------|
| `sprint-goals.md` | Goals for each sprint at a glance |
| `refinement/` | Refinement session notes — scope, acceptance criteria, estimates |
| `review/` | Sprint review notes — what was demoed, feedback received |
| `retrospective/` | Retrospective notes — what went well, what to improve |
| `_templates/` | Blank templates for each artifact type |

---

## guides/

Technical reference for working on this project. See [`guides/README.md`](guides/README.md) for the full breakdown.

| Folder | Purpose |
|--------|---------|
| `conventions/` | Project-wide rules — commits, coding style, naming, API organization, test conventions |
| `tooling/` | Tool usage — Git, Docker, pnpm, Turborepo, monorepo |
| `infra/` | Infrastructure setup — environment variables, Docker, GCP, GitHub Actions, test infrastructure |
| `tutorials/backend/` | Backend learning guides — FastAPI, SQLAlchemy, Alembic, auth flow, testing |
| `tutorials/frontend/` | Frontend learning guides — Vite, TypeScript, Vitest, Tailwind, ESLint, Docker, packages, openapi-typescript, services and constants, environment variables |
