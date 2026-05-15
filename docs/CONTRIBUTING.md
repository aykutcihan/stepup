# StepUp – Contributing Guide

## Branch Strategy

```
main       – production (merged only at sprint end)
develop    – integration branch (all PRs target this)
feature/   – new features   (feature/us-020-reports)
fix/       – bug fixes      (fix/login-redirect)
```

### Rules

- Never push directly to `main` or `develop`
- Open a **feature branch** for every change
- All PRs target `develop`
- `develop → main` merge happens only at sprint end

---

## Starting a New Feature

```bash
git checkout develop
git pull
git checkout -b feature/us-XXX-short-description
```

---

## Commit Guidelines

Write small, meaningful commits:

```
feat: add CSV export to reports page
fix: correct redirect param name in login
test: add E2E tests for task workflow
chore: update dependencies
docs: add deployment guide
```

---

## Pull Request Process

1. Push your branch
2. Open a PR targeting `develop`
3. Fill in the PR template (what changed, how to test)
4. Do not request review until CI is green
5. Get at least **1 approval**
6. Merge after approval

---

## CI Checks

Run automatically on every PR:

| Check | Description |
|-------|-------------|
| `test-backend` | pytest backend tests |
| `test-frontend` | typecheck + lint + test + build |

Merging is blocked when CI is red (branch protection).

---

## Test Requirements

- New feature → at least **1 test** required
- Bug fix → add a test that reproduces the bug
- E2E tests live under `apps/frontend/tests/e2e/`

---

## Code Quality

### Backend
```bash
# Lint
cd apps/backend && ruff check .

# Test
docker exec stepup-backend python -m pytest --tb=short -q
```

### Frontend
```bash
cd apps/frontend

# Typecheck
pnpm typecheck

# Lint
pnpm lint

# Format
pnpm format

# Test
pnpm test
```

---

## New Developer Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd stepup

# 2. Create env file
cp .env.example .env
# Edit .env and fill in required fields

# 3. Start with Docker
docker compose up --build

# 4. Load seed data
docker compose run --rm seeder

# 5. Open http://localhost:3000
```
