# Monorepo

## What is a Monorepo?

Normally, backend and frontend live in separate repositories:

```
github.com/aykutcihan/stepup-backend
github.com/aykutcihan/stepup-frontend
```

This is called **polyrepo**. Each repository is independent —
separate `package.json`, separate dependencies, separate CI/CD pipelines.

A **monorepo** puts everything into a single repository:

```
github.com/aykutcihan/stepup
  apps/
    backend/
    frontend/
  packages/
    shared-types/
```

One repository, but each application still runs independently.

---

## Why We Chose Monorepo

| Benefit | Explanation |
|---|---|
| Single clone | `git clone` once, you have everything |
| Shared types | Define a type in `packages/shared-types`, use it in both backend and frontend |
| Single command | `docker-compose up` starts backend, frontend, and database together |
| Single GitHub link | Employers see everything — code, sprints, PRs — in one place |
| Single CI/CD | One GitHub Actions pipeline manages everything |

---

## Polyrepo vs Monorepo

| | Polyrepo | Monorepo |
|---|---|---|
| Repositories | Multiple | One |
| Clone | Clone each separately | Clone once |
| Shared code | Copy-paste or npm package | `packages/` folder |
| CI/CD | One pipeline per repo | One pipeline total |
| Used by | Small teams, microservices | Google, Meta, Vercel, Turborepo |

---

## Our Monorepo Structure

```
stepup/                        ← root (one GitHub repository)
  apps/
    backend/                   ← FastAPI application
    frontend/                  ← React application
  packages/
    shared-types/              ← TypeScript types shared between apps
  docs/                        ← all documentation
  docker-compose.yml           ← starts everything with one command
  turbo.json                   ← Turborepo configuration
  pnpm-workspace.yaml          ← tells pnpm about our packages
  package.json                 ← root package, shared scripts
```

---

## Key Concept: apps/ vs packages/

**`apps/`** — things that run. They are deployable applications.
- `apps/backend` → deployed to GCP Cloud Run
- `apps/frontend` → deployed to Firebase Hosting

**`packages/`** — things that are shared. They are not deployed on their own.
- `packages/shared-types` → TypeScript types used by both backend and frontend

---

## In Plain Terms

Think of the monorepo like a single office building:
- `apps/backend` is the server room on the ground floor
- `apps/frontend` is the reception area on the first floor
- `packages/shared-types` is the shared filing cabinet both floors use
- `docker-compose.yml` is the master switch that turns the whole building on

---
