# Zustand

## What It Does

Zustand is a global state store. State defined in Zustand is accessible from any component without prop drilling.

In this project, Zustand stores the logged-in user's info (id, email, name, role) after login and clears it on logout.

---

## Why Not React Context?

Context re-renders every component that consumes it when the value changes.
For auth state, that means every component in the tree re-renders on login/logout.

Zustand uses a subscription model — a component re-renders only when the specific piece of state it reads changes.

See ADR-003 for the full decision.

---

## Store Definition

`src/stores/authStore.ts`:

```typescript
import { create } from 'zustand'
import type { components } from '@/types/api'

type User = components['schemas']['UserResponse']

type AuthStore = {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}))
```

---

## Reading From the Store

```typescript
const user = useAuthStore((state) => state.user)
const role = useAuthStore((state) => state.user?.role)
```

The selector `(state) => state.user` subscribes only to `user`.
The component re-renders only when `user` changes — not on every store update.

---

## Writing to the Store

```typescript
const setUser = useAuthStore((state) => state.setUser)
const clearUser = useAuthStore((state) => state.clearUser)

// After login
setUser(response)

// On logout
clearUser()
```

---

## Important: Clear on Logout

Zustand state persists across route changes but is lost when the browser tab closes.
Always call `clearUser()` explicitly on logout — do not rely on tab close to clear auth state.

If you forget to clear, the next user who opens the app on the same browser will see the previous user's name and role until the next API call fails.
