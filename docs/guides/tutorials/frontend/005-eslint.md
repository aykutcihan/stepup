# ESLint

## What is ESLint?

ESLint is a static analysis tool for JavaScript and TypeScript. It finds problems in code before the code runs — unused variables, unsafe patterns, broken React hooks usage.

---

## Flat Config (ESLint 9)

ESLint 9 introduced a new configuration format called "flat config". Our `eslint.config.js` uses this format.

**Old format (`.eslintrc.json`):**
```json
{
  "extends": ["eslint:recommended", "plugin:react-hooks/recommended"],
  "rules": {}
}
```

**New flat config (`eslint.config.js`):**
```javascript
export default [
  { rules: { ... } }
]
```

The flat config is a JavaScript array of config objects. Each object applies rules to matching files. More explicit, more composable, easier to understand what applies where.

---

## Our eslint.config.js Explained

```javascript
import js from '@eslint/js'
import reactHooks from 'eslint-plugin-react-hooks'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
    },
  },
)
```

### `tseslint.config()`

A helper from `typescript-eslint` that wraps the flat config array. It provides type safety for config objects and handles TypeScript-specific setup (parser, type-aware rules).

### `{ ignores: ['dist'] }`

Skip the build output folder. No need to lint compiled files.

### `extends: [js.configs.recommended, ...tseslint.configs.recommended]`

Two rule sets applied together:

**`js.configs.recommended`** → ESLint's built-in recommended rules. Catches common JavaScript errors: no-undefined-variables, no-duplicate-keys, no-unreachable-code, etc.

**`tseslint.configs.recommended`** → TypeScript-specific rules. Catches TypeScript-specific issues: no `any`, no unused variables with proper TypeScript handling, consistent type assertions.

### `files: ['**/*.{ts,tsx}']`

This config object only applies to `.ts` and `.tsx` files. TypeScript rules are not applied to `.js` config files like `eslint.config.js` itself.

### `eslint-plugin-react-hooks`

Rules for React Hooks. Two important rules:

**`rules-of-hooks`** → Hooks must only be called at the top level of a React component or custom hook. Not inside conditions, loops, or nested functions.

```typescript
// Error: hook called conditionally
if (user) {
  const [count, setCount] = useState(0)  // ❌
}

// Correct
const [count, setCount] = useState(0)    // ✅
if (user) { ... }
```

**`exhaustive-deps`** → `useEffect` and `useCallback` dependency arrays must list all variables they reference.

```typescript
// Error: count is used but not in deps
useEffect(() => {
  console.log(count)     // ❌ count missing from deps
}, [])

// Correct
useEffect(() => {
  console.log(count)     // ✅
}, [count])
```

This prevents stale closure bugs — one of the most common React mistakes.

---

## Running ESLint

```powershell
pnpm lint
```

This runs `eslint src` — checks all files inside `src/`.

ESLint is also enforced in CI: the pipeline runs `pnpm lint` on every PR and blocks merge on failure.
