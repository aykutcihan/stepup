# 03 — Turborepo

## What is Turborepo?

In a monorepo, you have multiple applications — backend, frontend, shared-types.
You want to run, test, and build all of them together.

Without Turborepo, you would do this manually:

```powershell
cd apps/backend && pnpm dev           # terminal 1
cd apps/frontend && pnpm dev          # terminal 2
cd packages/shared-types && pnpm build # terminal 3
```

Separate terminal for each app, separate command, manual order tracking.

Turborepo solves this with a single command from the root:

```powershell
pnpm dev   # starts everything
```

---

## What is a Build?

The code you write — TypeScript, Python — cannot be run directly by a computer.
**Build** = the process of converting your code into something runnable.

```
TypeScript code (you write this)
        ↓ build
JavaScript code (browser / Node.js runs this)
```

Real world analogy:
- Raw fruit = TypeScript source code
- Fruit juice = build output
- Squeezing = the build process

**Backend (Python/FastAPI):** Build is simpler — packages files and dependencies together.

**Frontend (React/TypeScript):** Build is more complex — converts TypeScript → JavaScript,
minifies files, optimizes for production.

---

## What is Cache?

Cache = storing the result of work you already did, so you don't repeat it.

Real world analogy:
- Yesterday you squeezed fruit juice and put it in the fridge
- Today the fruit hasn't changed — take it from the fridge, don't squeeze again
- Only squeeze again if the fruit changes

Turborepo cache works the same way:

```
Day 1: backend build → took 30 seconds → result saved to cache
Day 2: backend code unchanged → taken from cache → 0.1 seconds
Day 3: backend code changed → built again → 30 seconds
```

This saves a huge amount of time in CI/CD pipelines.

---

## Turborepo's 3 Superpowers

### 1. Dependency Ordering

`shared-types` must be built before `backend` and `frontend` can use it.
Turborepo understands this automatically:

```
shared-types build → backend build → frontend build
```

You just run `pnpm build` — Turborepo figures out the correct order.

### 2. Caching

If a package hasn't changed, Turborepo skips it and uses the cached result:

```
backend unchanged  → from cache (0.1 seconds)
frontend changed   → rebuild (30 seconds)
```

### 3. Parallel Execution

Independent tasks run at the same time:

```
backend tests  ─┐
frontend tests ─┤ → all run in parallel
lint check     ─┘
```

---

## turbo.json Explained

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
```

### build task

```json
"build": {
  "dependsOn": ["^build"],
  "outputs": ["dist/**"]
}
```

| Key | Meaning |
|---|---|
| `dependsOn: ["^build"]` | Before building this package, build all packages it depends on. `^` means "dependencies first" |
| `outputs: ["dist/**"]` | Build result goes into `dist/` folder — Turborepo caches this folder |

### dev task

```json
"dev": {
  "cache": false,
  "persistent": true
}
```

| Key | Meaning |
|---|---|
| `cache: false` | Do not cache in dev mode — always run fresh |
| `persistent: true` | Keep running, do not stop (development server runs continuously) |

### test task

```json
"test": {
  "dependsOn": ["^build"]
}
```

| Key | Meaning |
|---|---|
| `dependsOn: ["^build"]` | Before running tests, make sure all dependencies are built first |

---

## Root package.json Scripts

```json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test"
  }
}
```

When you run `pnpm dev` from the root:
1. pnpm reads `package.json` → finds `"dev": "turbo run dev"`
2. Turborepo reads `turbo.json` → finds the `dev` task definition
3. Turborepo runs `pnpm dev` in every app that has a `dev` script
4. All apps start in parallel

---

## Common Turborepo Commands

```powershell
pnpm dev                              # start all apps in dev mode
pnpm build                            # build all apps
pnpm test                             # run all tests
pnpm lint                             # lint all apps

turbo run dev --filter=backend        # run only backend
turbo run test --filter=frontend      # test only frontend
turbo run build --filter=shared-types # build only shared-types
```

---

## In Plain Terms

Think of Turborepo as a construction site manager:
- Without Turborepo: you personally tell each worker what to do, in what order, one by one
- With Turborepo: the manager knows who depends on whom, starts everyone at the right time, remembers what was already done (cache), and runs independent workers in parallel