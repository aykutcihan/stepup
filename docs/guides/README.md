# Guides

This directory contains all technical guides for the StepUp project.

## Structure

| Folder | Purpose |
|--------|---------|
| `tutorials/backend/` | Backend learning guides — FastAPI, SQLAlchemy, Alembic, auth flow |
| `tutorials/frontend/` | Frontend learning guides — React, routing, state management (coming soon) |
| `conventions/` | Project-wide rules — commit messages, coding style, schema naming, API organization |
| `tooling/` | Tool usage — Git, Docker, pnpm, Turborepo, monorepo |
| `infra/` | Infrastructure setup — environment variables, GCP, GitHub Actions, Docker |

## Numbering

Files within each folder are numbered by importance or learning order (e.g. `001-`, `002-`).

## Commit Scope Convention

When writing tests, prefix the scope with `be-` or `fe-` to distinguish backend from frontend:

```
test(be-us-001): add unit tests for invitation service
test(fe-us-001): add component tests for invite form
```
