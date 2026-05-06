# .npmrc

## What is .npmrc?

`.npmrc` is pnpm's configuration file.
It controls how pnpm behaves — how it installs packages, what rules it follows.

---

## Our .npmrc

```
shamefully-hoist=true
strict-peer-dependencies=false
```

---

## shamefully-hoist=true

### How pnpm normally works (strict mode)

By default, pnpm is very strict about package isolation.
Each package can only see its own `node_modules` — not anyone else's.

```
apps/
  backend/
    node_modules/
      express/        ← backend can see this
  frontend/
    node_modules/
      react/          ← frontend can see this
                      ← backend CANNOT see react (strict isolation)
```

This is safe and correct — but some older libraries do not expect this.
They assume packages are available globally and crash with "module not found" errors.

### What shamefully-hoist=true does

It moves some packages up to the root `node_modules/` so they are accessible to all apps:

```
node_modules/         ← root (shared, hoisted packages here)
  some-old-library/
apps/
  backend/
    node_modules/     ← backend-specific packages
  frontend/
    node_modules/     ← frontend-specific packages
```

Real world analogy:
- Strict mode: Every employee can only open their own locker
- `shamefully-hoist=true`: There is also a shared cabinet everyone can access

### Why "shamefully"?

The name is intentional — pnpm considers hoisting a bad practice.
It is called "shameful" because it breaks strict isolation.
But it is a necessary compromise for compatibility with older libraries.

---

## strict-peer-dependencies=false

### What is a peer dependency?

A peer dependency means:
"This library needs another library to be installed alongside it."

Example: `react-dom` requires `react` to also be installed.
If `react` is missing, `react-dom` complains.

### What strict-peer-dependencies=true does

If a peer dependency is missing → installation completely stops with an error.

```
pnpm install
→ ERROR: react-dom requires react@^18.0.0 but it is not installed
→ Installation failed
```

### What strict-peer-dependencies=false does

If a peer dependency is missing → installation continues with just a warning.

```
pnpm install
→ WARN: react-dom requires react@^18.0.0 but it is not installed
→ Installation completed
```

### Why we set it to false

During development, many libraries do not keep their peer dependency
declarations up to date. Getting hard errors for every outdated declaration
is frustrating and slows down development.

Setting it to `false` means:
- You still get warnings (so you know something is off)
- But installation does not fail completely
- You can fix peer dependency issues gradually

---

## Other Common .npmrc Settings

These are not in our file now but good to know:

```
# Always save exact versions (no ^ or ~)
save-exact=true

# Store packages in a custom location
store-dir=C:\pnpm-store

# Auto install peer dependencies
auto-install-peers=true
```

---

## In Plain Terms

`.npmrc` is like the house rules for pnpm:
- `shamefully-hoist=true` → "Common items go in the shared kitchen, not just personal rooms"
- `strict-peer-dependencies=false` → "If someone forgets to bring something, warn them but don't cancel the whole event"