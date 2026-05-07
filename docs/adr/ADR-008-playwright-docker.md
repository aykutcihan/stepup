# ADR-008: Playwright E2E Tests in a Dedicated Docker Container

**Date:** 2026-05-07
**Status:** Accepted

---

## Context

Sprint 2 requires E2E tests covering login, registration, and role-based routing. Playwright needs browser binaries (Chromium, Firefox, WebKit) and their system-level dependencies to run.

The frontend runs in a `node:18-slim` Docker container. Two options were considered for running Playwright tests in the local Docker environment.

---

## Decision

We run Playwright tests in a **dedicated Docker service** using the official `mcr.microsoft.com/playwright` image, added to `docker-compose.yml`.

```yaml
playwright:
  image: mcr.microsoft.com/playwright:v1.49.0-noble
  volumes:
    - ./apps/frontend:/app
  working_dir: /app
  depends_on:
    - frontend
    - backend
```

Run command:
```powershell
docker-compose run --rm playwright pnpm e2e
```

---

## Alternatives Considered

**Install Playwright inside the frontend container (`node:18-slim`)**

`node:18-slim` is a minimal image with no browser dependencies. Installing Playwright inside it requires adding dozens of system packages (`libglib2.0-0`, `libnss3`, `libatk1.0-0`, and many more). This bloats the image, increases build time, and makes the Dockerfile harder to maintain. The browser binaries also need to be downloaded separately on every image rebuild.

---

## Consequences

**Gained:**
- Frontend container stays clean — no browser dependencies or Playwright binaries
- Official Playwright image has all browser dependencies pre-installed and versioned
- Same pattern as backend tests: `docker-compose run --rm backend pytest` → `docker-compose run --rm playwright pnpm e2e`
- Playwright version is pinned via the image tag — consistent across all environments

**Trade-offs:**
- One additional service in `docker-compose.yml`
- First run pulls the Playwright image (~1.5GB) — one-time cost
