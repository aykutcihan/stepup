# React Router

## What It Does

Client-side routing — navigating between pages without a full page reload.
The URL changes, React renders a different component, but the browser never fetches a new HTML file from the server.

---

## Setup

`BrowserRouter` wraps the entire app in `main.tsx`:

```tsx
<BrowserRouter>
  <App />
</BrowserRouter>
```

Route definitions live in `App.tsx`:

```tsx
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />
  <Route path="/hr/invite-user" element={<InviteUserPage />} />
</Routes>
```

Each `Route` maps a URL path to a component. When the URL matches, that component renders.

---

## useNavigate — Redirect Programmatically

```tsx
import { useNavigate } from 'react-router-dom'

const navigate = useNavigate()
navigate('/login')         // go to login page
navigate('/hr/dashboard')  // go to dashboard
navigate(-1)               // go back (browser history)
```

**Used after login** to redirect based on role:

```tsx
async function onSubmit(data: FormData) {
  const user = await login(data)
  if (user.role === 'HR_ADMIN') navigate('/hr/dashboard')
  else if (user.role === 'MANAGER') navigate('/manager/dashboard')
  else navigate('/employee/dashboard')
}
```

---

## useParams — Read Dynamic Route Segments

```tsx
import { useParams } from 'react-router-dom'

const { id } = useParams<{ id: string }>()
```

**Used when the route has a variable segment:**

```tsx
// App.tsx
<Route path="/hr/templates/:id" element={<TemplateDetailPage />} />

// URL: /hr/templates/abc-123
// id → 'abc-123'
```

The segment name (`:id`) must match the key in `useParams`. TypeScript type parameter makes `id` typed as `string | undefined` — always guard against `undefined`:

```tsx
useEffect(() => {
  if (!id) return
  getTasks(id).then(setTasks)
}, [id])
```

**Difference from `useSearchParams`:**

| | `useParams` | `useSearchParams` |
|---|---|---|
| URL shape | `/templates/abc-123` | `/register?token=abc-123` |
| Use case | Identify a resource | Optional filters or tokens |
| Value always present | Yes (if route matches) | No — `.get()` can return null |

---

## useSearchParams — Read URL Query Parameters

```tsx
import { useSearchParams } from 'react-router-dom'

const [searchParams] = useSearchParams()
const token = searchParams.get('token')  // reads ?token=abc123
```

**Used in `RegisterPage`** to read the invitation token from the URL:

```
URL: /register?token=abc123
token → 'abc123'
```

If the param is missing, `.get()` returns `null`.
