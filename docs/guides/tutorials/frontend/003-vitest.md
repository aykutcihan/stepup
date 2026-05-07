# Vitest

## What is Vitest?

Vitest is a test runner built on top of Vite. It runs unit and component tests for the frontend.

The key advantage over Jest: Vitest shares Vite's config and transformation pipeline. You write tests in TypeScript with JSX — no separate Babel config needed.

---

## Why Not Jest?

Jest requires separate configuration to understand TypeScript and JSX. You need `ts-jest` or `babel-jest` plus configuration to make it work with modern ES modules.

Vitest works out of the box with Vite projects — it uses the same transforms Vite already has configured.

---

## Our vitest.config.ts Explained

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
})
```

### Why a Separate Config File?

See `001-vite.md` — Vitest bundles its own Vite version internally. Putting `test` config in `vite.config.ts` causes TypeScript type conflicts between Vitest's internal Vite and the project's installed Vite.

Keeping them separate eliminates the conflict. `vitest.config.ts` imports from `vitest/config`, `vite.config.ts` imports from `vite`.

### `plugins: [react()]`

Tests can contain JSX (React components). The React plugin is required to transform JSX in test files — same reason it is in `vite.config.ts`.

### `resolve.alias`

The `@/` path alias must be defined here too, otherwise tests that import from `@/components/...` will fail to resolve.

---

## Test Options

### `environment: 'jsdom'`

Vitest runs in Node.js, which has no browser APIs. `jsdom` is a JavaScript implementation of browser APIs — it provides `document`, `window`, `HTMLElement`, etc.

This is what makes it possible to test React components in Node.js. React Testing Library renders components into a jsdom environment.

Without this setting, tests that reference `document` or `window` would throw `ReferenceError`.

### `globals: true`

Makes test functions available globally without importing them:

```typescript
// Without globals: true
import { describe, it, expect } from 'vitest'

// With globals: true
describe('LoginForm', () => {
  it('renders email input', () => {
    expect(...)
  })
})
```

The `"types": ["vitest/globals"]` in `tsconfig.json` provides TypeScript types for these globals.

### `setupFiles: ['./tests/setup.ts']`

Runs this file before every test suite. Used to configure the test environment.

---

## tests/setup.ts Explained

```typescript
import '@testing-library/jest-dom'
```

Imports custom matchers from `@testing-library/jest-dom`. These extend Vitest's `expect` with DOM-specific assertions:

```typescript
expect(button).toBeInTheDocument()
expect(input).toHaveValue('hello@example.com')
expect(errorMessage).toBeVisible()
expect(submitButton).toBeDisabled()
```

Without this import, you would need to use lower-level DOM assertions. With it, tests read more like plain English.

---

## Test File Conventions

Tests live in `tests/` at the same level as `src/`, mirroring the `src/` structure:

```
apps/frontend/
  src/
    pages/
      LoginPage.tsx
    components/
      RequireRole.tsx
  tests/
    setup.ts
    pages/
      LoginPage.test.tsx
    components/
      RequireRole.test.tsx
```

---

## Running Tests

```powershell
# Run once (CI mode)
pnpm test

# Watch mode (development)
pnpm test:watch
```

Both commands use `vitest.config.ts` explicitly via `--config vitest.config.ts`.
