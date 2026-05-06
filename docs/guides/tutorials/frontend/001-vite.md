# Vite

## What is Vite?

Vite is a build tool for frontend applications. It serves your code in development and bundles it for production.

The name is French for "fast" — and that is the main point.

---

## Why Not Webpack?

Webpack was the standard for years. But it has a fundamental performance problem.

**Webpack approach:**
```
All files → bundle everything → start dev server
```

When you save a file, Webpack re-bundles everything from scratch. On a large project this takes 30–60 seconds per change.

**Vite approach:**
```
Start dev server immediately → serve files on demand (ESM)
```

Vite uses the browser's native ES module support. It does not bundle during development at all. The browser asks for a file, Vite serves just that file — instantly.

```
Webpack cold start: ~30 seconds
Vite cold start:    ~300ms
```

For production builds, Vite uses Rollup (a mature bundler) under the hood.

---

## Our vite.config.ts Explained

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### `plugins: [react()]`

Vite is framework-agnostic by default. The `@vitejs/plugin-react` plugin adds React support:
- Transforms `.tsx` and `.jsx` files via Babel
- Enables React Fast Refresh (hot reload that preserves component state)

Without this plugin, Vite does not know what to do with JSX syntax.

### `resolve.alias`

```typescript
'@': path.resolve(__dirname, './src')
```

This maps `@` to the `src/` folder. Instead of:
```typescript
import { Button } from '../../../components/Button'
```

You write:
```typescript
import { Button } from '@/components/Button'
```

Works regardless of how deeply nested the file is. `@` always means `src/`.

`path.resolve(__dirname, './src')` converts the relative `./src` to an absolute path — required because Vite runs from the project root, not the file's location.

---

## Entry Points: index.html and main.tsx

### index.html

```html
<div id="root"></div>
<script type="module" src="/src/main.tsx"></script>
```

Vite's entry point is `index.html`, not a JavaScript file. This is different from Webpack.

The `type="module"` attribute tells the browser to treat the script as an ES module — enabling Vite's native ESM serving in development.

### main.tsx

```typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

`createRoot` is React 18's rendering API. It mounts the React application into the `<div id="root">` element in `index.html`.

`StrictMode` wraps the entire app. It does not affect production — in development it activates additional checks and warnings (double-invokes lifecycle methods to catch side effects).

---

## vite-env.d.ts

```typescript
/// <reference types="vite/client" />
```

This single line tells TypeScript about Vite-specific features:
- CSS module types (`import styles from './foo.module.css'`)
- Static asset imports (`import logo from './logo.png'`)
- Environment variable types (`import.meta.env.VITE_API_URL`)

Without this file, TypeScript would show an error when importing `.css` files in `.tsx` components.

---

## Two Config Files: vite vs vitest

We have `vite.config.ts` and `vitest.config.ts` as separate files.

**Why?**

Vitest bundles its own version of Vite internally. When `defineConfig` is imported from `vitest/config`, it uses Vitest's internal Vite types. When `@vitejs/plugin-react` is imported, it uses the project's installed Vite types. These two Vite versions have incompatible types.

Splitting the configs keeps each file's types consistent:
- `vite.config.ts` → imports from `vite`, no type conflict
- `vitest.config.ts` → imports from `vitest/config`, includes the React plugin for test transforms

See `003-vitest.md` for the test config details.
