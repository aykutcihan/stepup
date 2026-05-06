# pnpm

## What is pnpm?

pnpm is a **package manager** for JavaScript/Node.js projects.
It installs and manages dependencies (libraries) that your project needs.

You may already know `npm` — pnpm does the same job but works differently.

---

## npm vs pnpm

### How npm works

npm downloads the same package separately for every project:

```
stepup/
  apps/
    backend/
      node_modules/
        typescript/     ← 50MB
    frontend/
      node_modules/
        typescript/     ← 50MB (same package, downloaded twice!)
```

Same package, twice the disk space, twice the download time.

### How pnpm works

pnpm downloads each package once into a central store.
Every project links to the same file:

```
C:\Users\Aykut\.pnpm-store\
  typescript@5.0.0\    ← downloaded once, central store

stepup/
  apps/
    backend/
      node_modules/
        typescript → link (points to central store)
    frontend/
      node_modules/
        typescript → link (points to same file)
```

Half the disk space. Much faster installs.

---

## npm vs pnpm vs yarn Comparison

| | npm | yarn | pnpm |
|---|---|---|---|
| Speed | Slow | Medium | Fast |
| Disk usage | High | High | Low |
| Monorepo support | Basic | Good | Excellent |
| Strictness | Loose | Loose | Strict |
| Used by | Everyone | Meta | Turborepo, Vercel |

---

## Why We Chose pnpm

- **Turborepo recommends pnpm** — they work perfectly together
- **Monorepo performance** — one install command sets up everything
- **Strict dependency resolution** — prevents hidden dependency bugs
- **Less disk usage** — important when you have many packages

---

## pnpm-workspace.yaml

This file tells pnpm which folders are part of our workspace:

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

This means:
- Every folder inside `apps/` is a separate package (`backend`, `frontend`)
- Every folder inside `packages/` is a separate package (`shared-types`)
- pnpm manages all of them together from the root

---

## How Workspace Packages Connect

Because of `pnpm-workspace.yaml`, packages can reference each other:

```json
// apps/backend/package.json
{
  "dependencies": {
    "@stepup/shared-types": "workspace:*"
  }
}
```

```json
// apps/frontend/package.json
{
  "dependencies": {
    "@stepup/shared-types": "workspace:*"
  }
}
```

`workspace:*` means: "find this package inside our monorepo, not on npm."

---

## Common pnpm Commands

```powershell
pnpm install                        # install all dependencies (run from root)
pnpm add <package>                  # add package to current app
pnpm add <package> -w               # add package to root workspace
pnpm add <package> --filter backend # add package to specific app
pnpm remove <package>               # remove a package
pnpm update                         # update all packages
```

---

## Key Files

| File | Purpose |
|---|---|
| `pnpm-workspace.yaml` | Defines which folders are workspace packages |
| `pnpm-lock.yaml` | Auto-generated, locks exact versions — always commit this |
| `.npmrc` | pnpm configuration options |
| `node_modules/` | Installed packages — never commit this (in .gitignore) |

---

## In Plain Terms

Think of pnpm like a library:
- npm buys a new copy of every book for every reader
- pnpm keeps one copy in the library and lets everyone borrow it
- `pnpm-workspace.yaml` is the list of all the reading rooms in the building