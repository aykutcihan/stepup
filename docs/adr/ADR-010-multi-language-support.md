# ADR-010: Custom Translation System over react-i18next

**Date:** 2026-05-16
**Status:** Accepted

---

## Context

StepUp targets organisations in the Netherlands, so Dutch and English language support was required. The two standard approaches were:

1. **react-i18next** — the de-facto standard library for React i18n (backed by i18next)
2. **Custom translation system** — a lightweight in-house solution with no external dependency

---

## Decision

We built a custom translation system consisting of three pieces:

- **`languageStore.ts`** — Zustand store that reads/writes `localStorage` key `stepup-language`, following the exact same pattern as `themeStore.ts`
- **`translations.ts`** — A single `as const` object with `en` and `nl` keys, fully type-safe
- **`useTranslation()`** — A hook that reads the current language from the store and returns the correct translation object

---

## Reasons

### Against react-i18next

- **Bundle size** — react-i18next adds ~30 KB for two static language files. The benefit does not justify the cost at this scale.
- **Complexity** — react-i18next introduces an async initialisation step, a provider, namespace configuration, and interpolation syntax (`t('key', { count })`). All of this is overhead for a two-language toggle.
- **New dependency** — Every new dependency is a maintenance surface. For two languages, it is not worth it.

### For the custom system

- **Zero dependencies** — No new package to install, update, or audit.
- **Full type safety** — `translations.ts` uses `as const`. TypeScript enforces that every key exists in both languages at compile time. Accessing a missing key is a type error, not a runtime crash.
- **Same pattern as themeStore** — The language store is structurally identical to the existing theme store. No new patterns for the codebase to absorb.
- **Trivial to extend** — Adding a third language means adding one top-level key to `translations.ts`.

---

## Consequences

- All UI strings that need translation must be added to `translations.ts` manually — there is no extraction tool.
- Interpolation (e.g. plurals with counts) is handled by plain TypeScript functions in the translations object: `entries: (n: number) => \`${n} ${n === 1 ? 'entry' : 'entries'} found\``
- If the app ever needs more than ~3 languages or server-side string loading, migrating to react-i18next becomes the right call.

---

## Alternatives Considered

| Option | Reason rejected |
|--------|----------------|
| react-i18next | Unnecessary complexity and bundle weight for two static languages |
| Hardcoded strings with a lang prop | Not scalable, pollutes component signatures |
| JSON files per language | Requires a loader, loses TypeScript type safety |
