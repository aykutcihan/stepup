# ADR-003: State Management — Zustand + React Query

**Date:** 2026-05-05
**Status:** Accepted

---

## Context

A React frontend application manages two fundamentally different kinds of state:

**Server state** — data that lives on the server and is fetched over the network: tasks, users, invitations, plans. This data can be stale, needs to be synchronized, has loading and error states, and can be refetched.

**Client state** — UI state that lives only in the browser: who is currently logged in, which modal is open, active tab selection. This does not need to be fetched or synchronized with the server.

These two categories have different requirements. Treating them the same way leads to unnecessary complexity.

We needed to choose:
1. One solution for both categories (Redux, Recoil, MobX)
2. Separate solutions for each category

---

## Decision

We use **React Query** (TanStack Query) for server state and **Zustand** for client state.

**React Query handles:**
- All API calls (GET, POST, PATCH, DELETE)
- Response caching and cache invalidation
- Loading, error, and success states
- Background refetching
- Optimistic updates (future)

**Zustand handles:**
- Logged-in user info (id, name, role) — stored after login, cleared on logout
- Nothing else in Sprint 2

---

## Alternatives Considered

### Redux Toolkit

Redux is the most widely known state management library. Redux Toolkit reduces boilerplate significantly compared to vanilla Redux.

However: Redux treats all state the same way — it has no concept of "this state comes from an API" vs "this state is local to the UI". Managing server state in Redux requires manual cache invalidation, manual loading/error tracking, and significant boilerplate (slices, thunks, selectors).

React Query solves the server state problem at the library level. Adding Redux on top for client state would mean maintaining two systems where React Query already handles 90% of the use cases.

**Decision: too much for what we need.**

### Context API

React's built-in Context API can share state across components without a third-party library.

However: Context re-renders all consumers when the value changes. For global auth state, this means every component reading from context re-renders on every login/logout event. This is acceptable for small apps but becomes a performance concern as the component tree grows.

Zustand uses a subscription model — only components that access a specific piece of state re-render when that piece changes.

**Decision: Zustand is better for auth state specifically.**

### Recoil / Jotai

Atom-based state libraries from Facebook/community. More granular than Zustand, good for complex interdependent state.

StepUp's client state is minimal — logged-in user and a few UI flags. The atom model is over-engineered for this use case.

**Decision: too complex for what we need.**

---

## Consequences

**Gained:**
- Server state is managed automatically — no manual loading/error/cache logic
- Cache invalidation is explicit: `queryClient.invalidateQueries(['invitations'])` after a mutation
- React Query DevTools shows all cached queries during development
- Zustand's store is simple to read and test — plain JavaScript object with functions
- Clear separation: API data goes through React Query, UI state goes through Zustand

**Trade-offs:**
- Two libraries to learn instead of one
- React Query has its own mental model (queryKey, stale time, refetch behavior) that takes time to internalize
- Zustand store must be cleared on logout — easy to forget

**Rule of thumb applied:**
> If the data comes from an API, it is server state → React Query.
> If the data never touches the server, it is client state → Zustand.

When in doubt, default to React Query. Avoid putting API data in Zustand.
