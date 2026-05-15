# Tailwind CSS

## What is Tailwind?

Tailwind is a utility-first CSS framework. Instead of writing custom CSS classes, you compose pre-built utility classes directly in HTML/JSX.

---

## Utility-First vs Traditional CSS

**Traditional CSS:**
```css
/* styles.css */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  background-color: white;
  border-radius: 8px;
}
```
```tsx
<form className="login-form">...</form>
```

**Tailwind:**
```tsx
<form className="flex flex-col gap-4 p-6 bg-white rounded-lg">...</form>
```

No separate CSS file. The styles are inline, but standardized.

---

## Why Tailwind?

**No naming problem.** Naming CSS classes is hard. `.card`, `.card-wrapper`, `.card-container` — naming collisions and decision fatigue. With Tailwind, there are no custom names.

**No dead CSS.** Traditional CSS accumulates unused classes over time. Tailwind's purge (via content scanning) removes unused utilities at build time — only used classes end up in the bundle.

**Consistency.** Tailwind uses a design system with a standardized scale (`p-4` = 16px, `p-6` = 24px, etc.). The design stays consistent across the app without manual coordination.

**Responsive design is built in.** Every utility can be prefixed with a breakpoint:
```tsx
<div className="flex-col md:flex-row">
```
Mobile: column layout. Medium screen and above: row layout.

---

## Our tailwind.config.js Explained

```javascript
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### `content`

Tailwind scans these files to find which utility classes are actually used. At build time, it removes all unused classes — the final CSS bundle only contains what is referenced.

```
'./index.html'          → scan the HTML entry point
'./src/**/*.{ts,tsx}'   → scan all TypeScript and TSX files in src/
```

If a class is not found in these files, it will not be in the production CSS.

### `theme.extend`

Add custom values on top of Tailwind's defaults. Currently empty — we use Tailwind's default design scale. Custom colors, spacing, or fonts would be added here as needed.

### `plugins`

Third-party Tailwind plugins. Currently empty. shadcn/ui does not require a plugin.

---

## Our postcss.config.js Explained

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

PostCSS is a tool that transforms CSS. Tailwind runs as a PostCSS plugin — it takes your `@tailwind` directives and generates the actual CSS.

**`tailwindcss`** → processes `@tailwind base/components/utilities` and generates all the utility classes.

**`autoprefixer`** → adds vendor prefixes where necessary (`-webkit-`, `-moz-`) for browser compatibility. You write standard CSS, autoprefixer handles compatibility automatically.

---

## src/index.css Explained

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Three directives that Tailwind replaces with generated CSS:

**`@tailwind base`** → Preflight — a CSS reset based on modern-normalize. Removes browser default margins, padding, and inconsistencies. Makes all browsers start from the same baseline.

**`@tailwind components`** → Component classes — Tailwind's pre-built component styles. Mostly empty in the default setup unless you add custom components.

**`@tailwind utilities`** → The utility classes (`flex`, `p-4`, `text-white`, etc.). This is the main output.

---

## Dark Mode

The project uses Tailwind's class-based dark mode strategy.

### Configuration

```javascript
// tailwind.config.js
export default {
  darkMode: 'class',  // ← dark: variants activate when <html> has class="dark"
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  ...
}
```

With `darkMode: 'class'`, every `dark:` prefixed utility only applies when an ancestor element has the `dark` class. In practice this means `<html class="dark">`.

> **Important:** After changing `darkMode` in `tailwind.config.js`, you must restart the Vite dev server. PostCSS reads the Tailwind config at startup and caches the CSS. Without a restart, dark: variants may still use the old strategy (`media` or none).

### Applying dark styles

Add a `dark:` variant alongside the light class:

```tsx
// background
<div className="bg-white dark:bg-gray-800">

// text
<p className="text-gray-900 dark:text-gray-100">

// border
<div className="border-gray-200 dark:border-gray-700">

// hover
<button className="hover:bg-gray-50 dark:hover:bg-gray-700">
```

### How the class is set

The `.dark` class on `<html>` is managed by `themeStore.ts`:

```typescript
export function applyTheme(theme: Theme) {
  const isDark =
    theme === 'dark' ||
    (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
  if (isDark) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}
```

An inline script in `index.html` also runs before React mounts to prevent a flash of the wrong theme on page load.

---

## The @tailwind Warnings in VSCode

VSCode's built-in CSS linter does not know about `@tailwind`. It shows yellow warnings: "Unknown at rule @tailwind".

These are **not errors** — they do not affect the build or runtime. To remove them, install the **Tailwind CSS IntelliSense** extension in VSCode. It teaches the CSS linter about Tailwind directives and also provides autocomplete for class names.
