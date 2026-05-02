# 04 — package.json

## What is package.json?

Every JavaScript/Node.js project has a `package.json` file.
It is the project's **identity card**:

- What is the project name
- What version is it
- What commands can you run
- What libraries does it need

---

## Two Types of package.json in Our Monorepo

```
stepup/
  package.json          ← ROOT: manages the entire monorepo
  apps/
    backend/
      package.json      ← APP: only backend dependencies and scripts
    frontend/
      package.json      ← APP: only frontend dependencies and scripts
  packages/
    shared-types/
      package.json      ← PACKAGE: only shared-types
```

**Root package.json** → runs Turborepo commands, manages the whole monorepo.
**App package.json** → manages one specific application.

This guide covers the **root package.json** only.
Each app's package.json will be covered when we build that app.

---

## Our Root package.json

```json
{
  "name": "stepup",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "turbo": "latest",
    "prettier": "^3.0.0"
  },
  "engines": {
    "node": ">=18",
    "pnpm": ">=8"
  },
  "packageManager": "pnpm@10.33.0"
}
```

---

## Field by Field

### name, version, private

```json
"name": "stepup"
```
The project name. Used internally by pnpm workspace.

```json
"version": "0.0.1"
```
Project version. Starts at 0.0.1 — not published anywhere yet.

```json
"private": true
```
Do not publish this package to npm.
Monorepo roots are always private — they are not meant to be published.

---

### scripts

```json
"scripts": {
  "build": "turbo run build",
  "dev": "turbo run dev",
  "lint": "turbo run lint",
  "test": "turbo run test",
  "format": "prettier --write \"**/*.{ts,tsx,md}\""
}
```

These are commands you can run from the terminal:

| Command | Runs | What happens |
|---|---|---|
| `pnpm dev` | `turbo run dev` | All apps start in development mode |
| `pnpm build` | `turbo run build` | All apps are built for production |
| `pnpm test` | `turbo run test` | All tests run across all apps |
| `pnpm lint` | `turbo run lint` | All code is checked for errors |
| `pnpm format` | `prettier --write` | All files are auto-formatted |

When you run `pnpm dev`, Turborepo takes over and starts
`backend`, `frontend`, and any other app that has a `dev` script.

---

### devDependencies

```json
"devDependencies": {
  "turbo": "latest",
  "prettier": "^3.0.0"
}
```

Packages only needed during development — not in production.

| Package | Purpose |
|---|---|
| `turbo` | Turborepo itself — runs and orchestrates all tasks |
| `prettier` | Code formatter — makes all code look consistent |

**dependencies vs devDependencies:**

| | dependencies | devDependencies |
|---|---|---|
| Needed in production | Yes | No |
| Example | express, react | turbo, prettier, eslint |
| Installed on server | Yes | No |

---

### engines

```json
"engines": {
  "node": ">=18",
  "pnpm": ">=8"
}
```

"This project requires Node.js 18 or higher, and pnpm 8 or higher."
If someone tries to run it with an older version, they get a warning.
This prevents "it works on my machine" problems.

---

### packageManager

```json
"packageManager": "pnpm@10.33.0"
```

"Use pnpm for this project, version 10.33.0."
If someone tries to use `npm install` or `yarn`, they get a warning.
This ensures everyone on the team uses the same package manager.

---

## Version Numbers Explained

You will see version numbers like `"^3.0.0"` and `"latest"` in package.json.

| Syntax | Meaning | Example |
|---|---|---|
| `"3.0.0"` | Exact version only | Only 3.0.0 |
| `"^3.0.0"` | Compatible updates allowed | 3.0.0, 3.1.0, 3.2.5 — but NOT 4.0.0 |
| `"~3.0.0"` | Patch updates only | 3.0.0, 3.0.1 — but NOT 3.1.0 |
| `"latest"` | Always the newest version | Whatever is current |
| `">=18"` | Minimum version | 18, 19, 20, 21... |

In production projects, avoid `"latest"` — pin to a specific version
so the project does not break when a new version is released.

---

## In Plain Terms

Root `package.json` is like a TV remote control:
- The remote itself does not show the picture (it is not an app)
- But it controls everything: volume up = `pnpm dev`, channel change = `pnpm build`
- Each TV (backend, frontend) has its own settings too — that is the app-level `package.json`