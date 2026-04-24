# ADR-005: Monorepo with Turborepo and pnpm

**Date:** 2026-04-21
**Status:** Accepted

---

## Context

StepUp has two applications — a FastAPI backend and a React frontend — that will eventually share TypeScript types via a shared package. The project needs a repository structure that keeps both apps in sync, makes running tasks (lint, test, build) straightforward, and is recognizable to employers reviewing the codebase.

Two structural options were considered: monorepo and polyrepo.

---

## Decision

We use a **monorepo** with **Turborepo** as the build orchestration tool and **pnpm** as the package manager.

```
stepup/
├── apps/
│   ├── backend/    # FastAPI
│   └── frontend/   # React
├── packages/
│   └── shared-types/
├── turbo.json
└── pnpm-workspace.yaml
```

---

## Alternatives Considered

**Polyrepo (separate repositories)**
Keeping backend and frontend in separate repositories is simpler to set up initially. However, it makes cross-app changes harder to track, requires managing two separate CI pipelines, and makes it impossible to share TypeScript types without publishing a package.

**Nx**
Nx is a powerful monorepo tool with more features than Turborepo (affected commands, project graph visualization). However, it has a steeper learning curve and heavier configuration. Turborepo is sufficient for a two-app monorepo and is faster to set up.

**Lerna**
Lerna is an older monorepo tool primarily designed for publishing npm packages. It is not the right fit for an application monorepo.

---

## Consequences

**Gained:**
- Single repository — one place for code, issues, PRs, and CI pipeline
- Turborepo caches task outputs — `turbo run build` only rebuilds what changed
- pnpm workspaces enable shared `packages/shared-types` without publishing to npm
- Single `docker-compose.yml` at the root runs both apps locally
- Employers see the full project in one repository

**Trade-offs:**
- pnpm PATH issue on Windows required a PowerShell profile fix (`$env:PATH += ...`)
- Turborepo adds a `turbo.json` configuration file that needs to be maintained