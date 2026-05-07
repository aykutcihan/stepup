# Frontend Architecture — How the Pieces Connect

Individual tutorials explain each tool in isolation. This document shows how they work together in a complete flow.

---

## The Tools and Their Roles

| Tool | Role | Tutorial |
|------|------|----------|
| `useState` | Local state — data used only inside one component | 011 |
| `useEffect` | Run code when a component first loads (e.g. fetch data) | 011 |
| `useForm` + Zod | Form input management and validation | 011 |
| Axios + `apiClient` | HTTP requests to the backend | 009 |
| Axios Interceptor | Catch 401 errors, refresh token, retry silently | 013 |
| Zustand (`useAuthStore`) | Global state — logged-in user info accessible everywhere | 014 |
| React Router (`useNavigate`) | Navigate to a different page after an action | 012 |

---

## The Login Flow — Step by Step

```
1. User fills email + password → useForm collects values

2. handleSubmit runs Zod validation
   → fails: show error messages, stop
   → passes: call onSubmit(data)

3. onSubmit calls authService.login(data)
   → Axios sends POST /api/v1/auth/login
   → Backend sets HttpOnly cookies, returns UserResponse

4. Login success:
   → setUser(response)         save user to Zustand store
   → navigate('/hr/dashboard') redirect based on role

5. Later — user visits a protected page:
   → Component calls an API (e.g. GET /invitations)
   → Access token cookie is sent automatically by the browser
   → Backend validates it, returns data

6. If access token expired:
   → Backend returns 401
   → Axios Interceptor catches it before the component sees it
   → Interceptor calls POST /api/v1/auth/refresh
       → Success: new cookies set, original request retried, component gets data
       → Failure: redirect to /login
```

---

## Where Each Tool Lives

```
src/
├── stores/
│   └── authStore.ts        ← Zustand: global user state
├── services/
│   ├── apiClient.ts        ← Axios instance + interceptor
│   └── authService.ts      ← login(), logout(), register()
└── pages/
    └── LoginPage.tsx       ← useForm + Zod + useNavigate + setUser
```

---

## useState vs Zustand — When to Use Which

| Situation | Use |
|-----------|-----|
| Form input values | `useState` (local, lives in the form component) |
| Error message on a page | `useState` (local, lives on that page) |
| Logged-in user info (name, role) | Zustand (global, needed in Navbar, Router, protected pages) |

Rule: if only one component needs it → `useState`. If multiple unrelated components need it → Zustand.

---

## The Prop Drilling Problem

Without Zustand, sharing user info across unrelated components requires passing it down through every level:

```
App (has user)
└── Layout (passes user)
    ├── Navbar (passes user)
    │   └── UserMenu (finally uses user)
    └── Routes (passes user)
        └── RequireRole (finally uses user)
```

Every component in between receives a prop it does not use — just to pass it down.

With Zustand, any component reads directly from the store:

```typescript
// In Navbar — no props needed
const user = useAuthStore((state) => state.user)

// In RequireRole — no props needed
const user = useAuthStore((state) => state.user)
```

---

## Page Refresh — Restoring Auth State

Zustand lives in memory. When the user refreshes the page, the store resets — `user` becomes `null`.

Without handling this, every page refresh would redirect to `/login` even if the user has a valid session cookie.

**Solution:** `App.tsx` calls `GET /me` on first render. If the cookie is still valid, the user is restored to Zustand before any route renders.

```typescript
useEffect(() => {
  getMe()
    .then(setUser)
    .catch(() => {})
    .finally(() => setLoading(false))
}, [])
```

**`isLoading` flag:** While `/me` is in flight, `RequireRole` must not redirect yet — it does not know if the user is logged in or not. The store starts with `isLoading: true`. After `/me` resolves (success or failure), it becomes `false`. `RequireRole` renders `null` until loading is done.

```
Page loads → isLoading: true → RequireRole renders null
→ /me resolves → isLoading: false
  → user set   → RequireRole shows the page
  → user null  → RequireRole redirects to /login
```

---

## Logout Flow

```
1. User clicks logout button
2. authService.logout() → POST /api/v1/auth/logout
3. Backend clears cookies, deletes refresh token from DB
4. clearUser()       ← clear Zustand store
5. navigate('/login')
```

Clearing Zustand on logout is critical — if skipped, the next page load still shows the previous user's name and role until an API call fails.
