# TypeScript Configuration

## What is tsconfig.json?

`tsconfig.json` tells the TypeScript compiler how to treat your code. It controls:
- Which JavaScript features to compile down to
- How strict the type checking is
- Where to find files
- How to resolve module paths

---

## Our tsconfig.json Explained

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    },
    "types": ["node", "vitest/globals"]
  },
  "include": ["src", "vite.config.ts"],
  "exclude": ["node_modules"]
}
```

---

## Target and Output

### `"target": "ES2020"`

The JavaScript version TypeScript compiles down to. ES2020 supports modern features (optional chaining, nullish coalescing, async/await) and is supported by all modern browsers.

### `"lib": ["ES2020", "DOM", "DOM.Iterable"]`

TypeScript's built-in type definitions to include:
- `ES2020` → JavaScript standard library types (Promise, Map, Set, etc.)
- `DOM` → browser API types (document, window, HTMLElement, etc.)
- `DOM.Iterable` → iteration over DOM collections (NodeList, HTMLCollection)

Without `DOM`, TypeScript would not know what `document.getElementById()` is.

### `"module": "ESNext"` and `"moduleResolution": "bundler"`

`module: ESNext` means TypeScript emits ES module syntax (`import`/`export`). Vite handles the actual bundling.

`moduleResolution: bundler` is a TypeScript 5 mode designed for bundlers like Vite and esbuild. It allows importing files without writing the extension:
```typescript
import { foo } from './utils'   // resolves to ./utils.ts
```

---

## Strict Mode

### `"strict": true`

Enables a bundle of strict checks. The most important ones:
- `strictNullChecks` → `null` and `undefined` are not assignable to other types unless explicitly allowed
- `noImplicitAny` → every variable must have a known type

```typescript
// Without strict
function greet(name) {          // name has type 'any' — TypeScript cannot help
  return name.toUppercase()     // typo: toUppercase vs toUpperCase — no error
}

// With strict
function greet(name: string) {  // explicit type required
  return name.toUppercase()     // Error: Property 'toUppercase' does not exist
}
```

Strict mode catches bugs before they reach production.

### `"noUnusedLocals": true` and `"noUnusedParameters": true`

Errors on declared-but-never-used variables and function parameters. Keeps the code clean.

### `"noFallthroughCasesInSwitch": true`

Errors on `switch` cases that fall through to the next case without a `break`. A common source of bugs.

---

## Build Configuration

### `"noEmit": true`

TypeScript does not produce any `.js` output files. Vite handles transpilation. TypeScript's only job here is type checking.

### `"isolatedModules": true`

Each file must be independently transpilable — no cross-file type inference at transpile time. Required by Vite and esbuild, which process files one at a time for speed.

### `"skipLibCheck": true`

Skip type checking of `.d.ts` files in `node_modules`. Many libraries have slightly incorrect type definitions. This flag prevents those errors from blocking compilation.

### `"allowImportingTsExtensions": true`

Allows writing `.ts` or `.tsx` extensions in imports:
```typescript
import { foo } from './utils.ts'  // allowed
```

Needed because `noEmit: true` means TypeScript is not changing the extensions — Vite handles that.

---

## JSX

### `"jsx": "react-jsx"`

Tells TypeScript which JSX transform to use. `react-jsx` is the modern React 17+ transform — you no longer need to `import React from 'react'` in every file that uses JSX.

---

## Path Alias

### `"paths": { "@/*": ["./src/*"] }`

Mirrors the alias defined in `vite.config.ts`. TypeScript uses this to resolve `@/` imports for type checking. Vite uses its own alias for bundling. Both must be configured to avoid errors.

```typescript
import { Button } from '@/components/Button'
// TypeScript resolves: ./src/components/Button.ts
// Vite resolves:       <project-root>/src/components/Button.tsx
```

---

## Types

### `"types": ["node", "vitest/globals"]`

Explicitly include:
- `node` → Node.js global types (`__dirname`, `process`, `Buffer`)
- `vitest/globals` → Vitest globals (`describe`, `it`, `expect`) without needing to import them

---

## include and exclude

```json
"include": ["src", "vite.config.ts"]
```

TypeScript only checks these paths. `vite.config.ts` is included so the config file itself is type-checked.

```json
"exclude": ["node_modules"]
```

Skip `node_modules` — types from libraries come through `@types/*` declarations, not by type-checking the source.
