# Playwright

## What is Playwright?

Playwright is an E2E (end-to-end) test framework. Unlike Vitest which tests components in isolation, Playwright launches a real browser, navigates to pages, fills forms, and clicks buttons — exactly as a user would.

---

## Why a Dedicated Docker Container?

Playwright needs browser binaries (Chromium, Firefox, WebKit) and their system-level dependencies to run. The frontend container uses `node:18-slim` which is a minimal image with none of these dependencies.

We use the official `mcr.microsoft.com/playwright` Docker image as a separate service in `docker-compose.yml`. This image has all browser dependencies pre-installed.

See ADR-008 for the full decision.

---

## Why `@playwright/test` in `package.json`?

Even though Playwright runs inside Docker, we add `@playwright/test` as a local devDependency:

```json
"@playwright/test": "^1.49.0"
```

Without it, TypeScript cannot resolve `defineConfig` in `playwright.config.ts` and the type declarations in test files:

```
Cannot find module '@playwright/test' or its corresponding type declarations.
```

The package runs inside the Docker container — the local install is only for TypeScript type checking. Same reason Vitest is listed in devDependencies even though tests run via pnpm scripts.

---

## Our `playwright.config.ts` Explained

```typescript
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://frontend:3000',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
})
```

### `testDir: './tests/e2e'`

E2E tests live in `tests/e2e/` — separate from unit tests which are co-located next to components. E2E tests test the full system, not a single component, so they don't belong next to any specific file.

### `baseURL: 'http://frontend:3000'`

The Playwright container reaches the frontend via Docker's internal network. `frontend` is the service name in `docker-compose.yml` — Docker resolves it to the container's IP automatically.

### `projects: [{ name: 'chromium' }]`

We run tests only in Chromium for now. Playwright supports Firefox and WebKit too — additional projects can be added later if cross-browser coverage is needed.

---

## Running E2E Tests

Start all services first, then run the Playwright container:

```powershell
# Start the full stack
docker-compose up -d db backend frontend

# Run E2E tests
docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"
```

---

## Test File Location

E2E tests live in `tests/e2e/` — not co-located with components:

```
apps/frontend/
  src/
    features/
      auth/
        pages/
          LoginPage.tsx
          LoginPage.test.tsx    ← unit test, co-located
  tests/
    setup.ts
    e2e/
      login.spec.ts             ← E2E test, separate
      register.spec.ts
```

**Why separate?** E2E tests test full user flows across multiple pages, not a single component. They have no natural "home" next to any one file.
