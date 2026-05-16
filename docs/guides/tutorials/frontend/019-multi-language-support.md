# Multi-Language Support

StepUp uses a lightweight custom translation system. No external library is required.

---

## How It Works

Three files form the entire system:

```
src/
  stores/languageStore.ts     ← Zustand store, persists to localStorage
  i18n/
    translations.ts           ← All strings for every language
    useTranslation.ts         ← Hook that returns the right translations
```

The language store reads `localStorage` on init and writes back on every change — the same pattern used by `themeStore`.

---

## Using Translations in a Component

```typescript
import { useTranslation } from '@/i18n/useTranslation'

export default function MyPage() {
  const t = useTranslation()

  return <h1>{t.nav.dashboard}</h1>
}
```

`t` is fully type-safe — accessing a key that doesn't exist in `translations.ts` is a compile-time error.

---

## Adding a New String

1. Open `src/i18n/translations.ts`
2. Add the key under **both** `en` and `nl`:

```typescript
export const translations = {
  en: {
    mySection: {
      myKey: 'Hello',
    },
  },
  nl: {
    mySection: {
      myKey: 'Hallo',
    },
  },
} as const
```

3. Use it in your component: `t.mySection.myKey`

TypeScript will give a compile error if the key is missing in either language.

---

## Strings with Dynamic Values

Use a plain function instead of a string:

```typescript
// translations.ts
entries: (n: number) => `${n} ${n === 1 ? 'entry' : 'entries'} found`,

// nl
entries: (n: number) => `${n} ${n === 1 ? 'vermelding' : 'vermeldingen'} gevonden`,
```

Call it like a function in the component:

```tsx
<p>{t.audit.entries(total)}</p>
```

---

## Adding a Third Language

1. Add a new top-level key to `translations.ts` (e.g. `de`)
2. Add `'de'` to the `Language` type in `languageStore.ts`
3. Add the option to `LANGUAGE_OPTIONS` in both layout files

---

## Where Language State Lives

`useLanguageStore` is a Zustand store — no React context, no provider needed. Any component can call `useLanguageStore` directly.

```typescript
import { useLanguageStore } from '@/stores/languageStore'

const { language, setLanguage } = useLanguageStore()
```

The selected language persists across page reloads via `localStorage` key `stepup-language`.
