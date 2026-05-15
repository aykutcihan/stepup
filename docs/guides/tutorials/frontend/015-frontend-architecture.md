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
| Zustand (`useThemeStore`) | Global state — selected theme (light/dark/system), persisted in localStorage | 014 |
| React Router (`useNavigate`) | Navigate to a different page after an action | 012 |
| React Router (`useParams`) | Read dynamic URL segments (e.g. `/templates/:id`) | 012 |

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
├── app/
│   ├── App.tsx             ← route definitions
│   └── useAuthInit.ts      ← auth state bootstrap on page load
├── stores/
│   ├── authStore.ts        ← Zustand: global user state
│   └── themeStore.ts       ← Zustand: theme selection (light/dark/system)
├── layouts/
│   ├── DashboardLayout.tsx     ← shared layout for Manager + Employee
│   └── HRDashboardLayout.tsx   ← HR Admin layout with sidebar
├── constants/
│   ├── apiEndpoints.ts     ← all API URL strings
│   ├── routes.ts           ← all frontend route paths
│   └── errorMessages.ts    ← error_code → human readable message map
└── features/
    ├── department/
    │   ├── services/
    │   │   └── departmentService.ts
    │   ├── hooks/
    │   │   └── useDepartmentsPage.ts
    │   └── pages/
    │       └── DepartmentsPage.tsx
    ├── template/
    │   ├── services/
    │   │   └── templateService.ts
    │   ├── hooks/
    │   │   ├── useTemplatesPage.ts      ← list page state
    │   │   └── useTemplateDetailPage.ts ← detail page state + useParams
    │   └── pages/
    │       ├── TemplatesPage.tsx
    │       └── TemplateDetailPage.tsx
    └── users/
        ├── services/
        │   └── userService.ts
        ├── hooks/
        │   ├── useUsersPage.ts
        │   └── useProfilePage.ts
        └── pages/
            ├── HRDashboard.tsx
            ├── UsersPage.tsx
            └── ProfilePage.tsx
```

---

## Feature-Based Folder Structure

Each feature lives under `features/<domain>/` and has three layers:

```
features/
└── department/
    ├── services/   ← talks to the API
    ├── hooks/      ← owns state and business logic
    └── pages/      ← renders what the hook gives it
```

**Why not flat?** When features grow, a flat `services/` and `pages/` folder mixes unrelated files. Feature folders keep everything for one domain together — easier to find, easier to delete if the feature is removed.

---

## Hook as Business Logic Container

Pages are dumb renderers. All state and logic lives in a hook:

```typescript
// ❌ Logic inside the page
export default function DepartmentsPage() {
  const [departments, setDepartments] = useState([])
  useEffect(() => { getDepartments().then(setDepartments) }, [])
  async function handleCreate() { ... }
  return <table>...</table>
}

// ✅ Logic in the hook, page only renders
export default function DepartmentsPage() {
  const { departments, handleCreate } = useDepartmentsPage()
  return <table>...</table>
}
```

**Why?** The page component becomes trivial to read. The hook is independently testable — you can mock services and test business logic without rendering any UI.

---

## Layout Routing Pattern

React Router v6 supports layout routes — a parent route that wraps children with a shared shell. The child page renders into `<Outlet />`.

```tsx
// App.tsx — three nested layers
<Route element={<RequireRole roles={[USER_ROLES.HR_ADMIN]} />}>   // auth guard
  <Route element={<HRDashboardLayout />}>                          // layout shell
    <Route path={ROUTES.HR_DASHBOARD} element={<HRDashboard />} />
    <Route path={ROUTES.HR_DEPARTMENTS} element={<DepartmentsPage />} />
  </Route>
</Route>
```

Each layer has one responsibility:
- `RequireRole` — checks auth, redirects if not allowed
- `HRDashboardLayout` — renders nav bar + sidebar + `<Outlet />`
- Page component — renders only its own content

**Before this pattern**, each page imported and wrapped itself in the layout:
```tsx
// ❌ Old — every page knows about the layout
export default function DepartmentsPage() {
  return (
    <DashboardLayout>
      <div>content</div>
    </DashboardLayout>
  )
}
```

**After**, pages know nothing about the layout:
```tsx
// ✅ New — page is just content
export default function DepartmentsPage() {
  return <div>content</div>
}
```

---

## Role-Based Layouts

Different roles use different layouts. HR Admin has a sidebar, others have a simple top bar:

```
Manager / Employee  →  DashboardLayout     (top bar only)
HR Admin            →  HRDashboardLayout   (top bar + sidebar)
```

This is achieved by wrapping each role's route group with its own layout route. No conditional rendering inside the layout — each layout is simple and knows only its own structure.

---

## useState vs Zustand — When to Use Which

| Situation | Use |
|-----------|-----|
| Form input values | `useState` (local, lives in the form component) |
| Error message on a page | `useState` (local, lives on that page) |
| Logged-in user info (name, role) | Zustand (global, needed in Navbar, Router, protected pages) |
| Selected theme (light/dark/system) | Zustand (global, needed in every layout and ThemeProvider) |

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

## Dynamic Routes — Detail Pages

Some pages display a single resource identified by an ID in the URL:

```
/hr/templates         → list of all templates
/hr/templates/abc-123 → detail page for one template
```

The route is defined with a `:id` segment in `App.tsx`:

```tsx
<Route path="/hr/templates/:id" element={<TemplateDetailPage />} />
```

The page reads the ID with `useParams`:

```tsx
const { id } = useParams<{ id: string }>()
```

The hook uses `id` to fetch the specific resource on mount:

```tsx
useEffect(() => {
  if (!id) return
  getTemplate(id).then(setTemplate)
  getTasks(id).then(setTasks)
}, [id])
```

Navigation to a detail page uses the route constant:

```tsx
// routes.ts
HR_TEMPLATE_DETAIL: (id: string) => `/hr/templates/${id}`

// In the list page
<Link to={ROUTES.HR_TEMPLATE_DETAIL(t.id)}>View</Link>
```

See `018-ui-patterns.md` for the kebab menu and table overflow patterns used on list and detail pages.

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
