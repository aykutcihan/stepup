# Environment Variables

## The Problem With Hardcoded URLs

```typescript
// ❌ Wrong — only works on one machine
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
})
```

This breaks when:
- Another developer clones the project (their BE might be on a different port)
- The app is deployed to production (BE is no longer on localhost)
- Tests run against a staging environment

The solution: read the URL from an environment variable.

---

## How Vite Handles Environment Variables

Vite reads `.env` files and makes variables available in code via `import.meta.env`.

```
.env file:              Code:
VITE_API_URL=http://... → import.meta.env.VITE_API_URL
```

**The `VITE_` prefix is required.**

Vite only exposes variables that start with `VITE_` to the browser bundle. Variables without this prefix stay server-side only — they never reach the browser. This prevents accidentally leaking secrets.

```
VITE_API_URL=http://localhost:8000   ✅ Available in browser code
DATABASE_URL=postgresql://...        ❌ Never reaches browser — stays server-side
```

---

## Our Setup

### apps/frontend/.env

```
VITE_API_URL=http://localhost:8000
```

This file is in `.gitignore` — it is never committed. Each developer creates it locally.

### apps/frontend/.env.example

```
VITE_API_URL=http://localhost:8000
```

This file IS committed. It documents what variables are needed and their expected format. A developer cloning the project copies this file to `.env` and fills in their values.

```powershell
# After cloning the project
cp apps/frontend/.env.example apps/frontend/.env
# Edit .env with your local values
```

### Usage in code

```typescript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})
```

---

## .env vs .env.example — Why Two Files?

| File | Committed? | Purpose |
|---|---|---|
| `.env` | ❌ No | Actual values for your machine |
| `.env.example` | ✅ Yes | Template showing what variables exist |

`.env` contains real values — potentially sensitive (API keys, tokens). Never commit it.

`.env.example` contains placeholder values — safe to commit. Acts as documentation.

---

## TypeScript and import.meta.env

By default TypeScript does not know what variables exist in `import.meta.env`. To add type safety, add a `vite-env.d.ts` or extend the `ImportMetaEnv` interface:

Our `src/vite-env.d.ts` already includes `/// <reference types="vite/client" />` which gives basic typing. For stricter typing per variable, you can extend:

```typescript
// vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}
```

This makes TypeScript error if `VITE_API_URL` is missing — caught at compile time, not runtime.
