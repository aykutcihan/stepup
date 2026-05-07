# Services and Constants

## The Problem With Magic Strings

Without constants, API URLs and route paths are written as raw strings scattered across the codebase:

```typescript
const res = await axios.get('/api/v1/invitations/validate?token=' + token)
navigate('/login')
```

Two problems:
- **Duplication** — the same string in 10 files. Change the URL, find and fix 10 places.
- **Typo risk** — `/api/v1/invitations/valiidate` compiles fine, fails at runtime.

Constants solve both.

---

## src/constants/apiEndpoints.ts

All API endpoint strings in one place.

```typescript
export const API = {
  INVITATIONS: {
    VALIDATE: '/api/v1/invitations/validate',
  },
  AUTH: {
    REGISTER: '/api/v1/auth/register',
  },
}
```

Usage:
```typescript
axios.get(API.INVITATIONS.VALIDATE, { params: { token } })
axios.post(API.AUTH.REGISTER, data)
```

**Rule:** Add an entry here when a new endpoint is used in the FE. Never write raw endpoint strings elsewhere.

New entries are added as needed — one US at a time. US-002 will add `AUTH.LOGIN`, `AUTH.LOGOUT`, `AUTH.REFRESH`. Not before.

---

## src/constants/routes.ts

All frontend page paths in one place. Split into two exports:

```typescript
export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  HR_DASHBOARD: '/hr/dashboard',
  MANAGER_DASHBOARD: '/manager/dashboard',
  EMPLOYEE_DASHBOARD: '/employee/dashboard',
}

export const ERROR_ROUTES = {
  FORBIDDEN: '/403',
}
```

`ROUTES` holds normal page paths. `ERROR_ROUTES` holds error page paths — kept separate so it is obvious at a glance which routes are error states.

Usage:
```typescript
navigate(ROUTES.LOGIN)
navigate(ROUTES.HR_DASHBOARD)
<Navigate to={ERROR_ROUTES.FORBIDDEN} />
<Route path={ROUTES.REGISTER} element={<RegisterPage />} />
```

**Rule:** Add an entry here when a new page route is created. Never write raw path strings elsewhere.

---

## src/constants/errorMessages.ts

Maps BE business logic error codes to user-facing messages.

```typescript
export const ERROR_MESSAGES: Record<string, string> = {
  INVITATION_EXPIRED: 'This invitation link has expired.',
  INVITATION_ALREADY_USED: 'This invitation link has already been used.',
  USER_ALREADY_EXISTS: 'An account with this email already exists.',
}
```

**Why this exists:**

BE returns:
```json
{ "error_code": "INVITATION_EXPIRED", "message": "Invitation token has expired" }
```

The FE does not show `message` from BE directly — that string is for logging. The FE shows its own user-facing string, looked up by `error_code`.

This separation means:
- BE messages can change without affecting the UI
- FE messages can be translated to another language by swapping this file

**Rule:** Add an entry here for every custom BE error code that the FE needs to display. Source of truth: `apps/backend/app/errors/messages.py`.

---

## src/constants/userRoles.ts

BE role values as typed constants — eliminates magic strings like `'hr_admin'` scattered across the codebase.

```typescript
export type UserRole = components['schemas']['UserRole']

export const USER_ROLE_VALUES = ['employee', 'manager', 'hr_admin'] as const satisfies readonly UserRole[]

export const USER_ROLES = {
  HR_ADMIN: 'hr_admin' as UserRole,
  MANAGER: 'manager' as UserRole,
  EMPLOYEE: 'employee' as UserRole,
}
```

**`USER_ROLE_VALUES`** — a tuple for Zod validation:
```typescript
role: z.enum(USER_ROLE_VALUES)
```

**`USER_ROLES`** — an object for comparisons:
```typescript
if (user.role === USER_ROLES.HR_ADMIN) navigate(ROUTES.HR_DASHBOARD)
```

**Rule:** Never write `'hr_admin'`, `'manager'`, or `'employee'` as raw strings. Use these constants.

---

## src/services/

Service files contain the actual API calls. They use `axios`, the constants from above, and the types from `api.ts`.

```
src/services/
  authService.ts      ← login, logout, register, validateInvitation, getMe
  invitationService.ts ← create, list, resend
  userService.ts      ← getUsers, deactivateUser
```

One file per domain — same grouping as BE routers.

---

## src/services/apiClient.ts

Every API call in the project goes through a single axios instance defined here.

```typescript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})

export default apiClient
```

### `axios.create()`

Creates a custom axios instance with preset configuration. All service functions import `apiClient` instead of raw `axios` — the base URL is set once, applied everywhere.

### `baseURL: import.meta.env.VITE_API_URL`

The BE address comes from an environment variable, not hardcoded. In development: `http://localhost:8000`. In production: the deployed Cloud Run URL.

If hardcoded, anyone cloning the project would need to edit source code to point at their BE — wrong approach.

### `withCredentials: true`

The BE uses HttpOnly cookies for auth tokens. Browsers block cookies on cross-origin requests by default (FE on port 3000, BE on port 8000 = different origins). This flag tells the browser: "send cookies on cross-origin requests."

Without this, login would succeed but every subsequent request would be unauthenticated.

### Why in `services/`?

`apiClient.ts` is the shared foundation all service files depend on. Keeping it in `services/` means one folder holds everything API-related. No separate `lib/` or `config/` folder needed.

---

## src/services/authService.ts Explained

```typescript
import apiClient from '@/services/apiClient'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type InvitationValidateResponse = components['schemas']['InvitationValidateResponse']
type RegisterRequest = components['schemas']['RegisterRequest']
type UserResponse = components['schemas']['UserResponse']

export async function validateInvitation(token: string): Promise<InvitationValidateResponse> {
  const res = await apiClient.get(API.INVITATIONS.VALIDATE, { params: { token } })
  return res.data
}

export async function register(data: RegisterRequest): Promise<UserResponse> {
  const res = await apiClient.post(API.AUTH.REGISTER, data)
  return res.data
}
```

### `apiClient.get` with `params`

```typescript
apiClient.get(API.INVITATIONS.VALIDATE, { params: { token } })
```

This sends: `GET /api/v1/invitations/validate?token=abc123`

`params` is an object — axios serializes it into the query string automatically.

### `Promise<InvitationValidateResponse>`

The return type tells TypeScript what shape `res.data` has. Without this, `res.data` is typed as `any` — no autocomplete, no type safety.

With it:
```typescript
const data = await validateInvitation(token)
data.email  // ✅ TypeScript knows this exists
data.xyz    // ❌ TypeScript error — xyz does not exist on InvitationValidateResponse
```

### Why not fetch()?

The browser has a built-in `fetch()`. Axios adds:
- Automatic JSON parsing (fetch requires `res.json()` manually)
- Interceptors — middleware for every request/response (used in US-002 for token refresh)
- Better error handling — axios throws on non-2xx status, fetch does not

---

## The Full Flow

```
User submits form
      ↓
RegisterPage calls authService.register(data)
      ↓
authService sends POST /api/v1/auth/register  (URL from apiEndpoints.ts)
      ↓
BE responds
      ↓
Success → navigate(ROUTES.LOGIN)              (path from routes.ts)
Error   → look up error_code in ERROR_MESSAGES (from errorMessages.ts)
        → show user-facing message
```

Every piece has one home. Nothing is hardcoded inline.

---

## RegisterPage — How It All Comes Together

RegisterPage is the first page that uses all these pieces together. Understanding it shows how services, constants, hooks, and types connect.

### Page load: useEffect + validateInvitation

```typescript
useEffect(() => {
  if (!token) {
    setPageError('Invalid or missing invitation link.')
    return
  }
  validateInvitation(token)
    .then((data) => setEmail(data.email))
    .catch((err) => {
      const code = err.response?.data?.error_code
      setPageError(ERROR_MESSAGES[code] ?? 'This invitation link is invalid.')
    })
}, [token])
```

**`useEffect`** runs after the component renders. The `[token]` dependency array means: "run this when `token` changes." On first render, `token` is read from the URL and this effect fires once.

**Why not call `validateInvitation` directly in the component body?**

React renders components many times. Calling an API directly in the component body would send a request on every render — potentially dozens of requests. `useEffect` with a dependency array ensures it runs only when needed.

**`.then()` and `.catch()`** are Promise callbacks:
- `.then(data => ...)` — runs when the API call succeeds
- `.catch(err => ...)` — runs when the API call fails

### Form submission: handleSubmit + onSubmit

```typescript
const { register: registerField, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
})

const onSubmit = async (data: FormData) => {
  try {
    await register({ token, ...data })
    navigate(ROUTES.LOGIN)
  } catch (err: unknown) {
    const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
    setPageError(ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong. Please try again.')
  }
}
```

**`handleSubmit(onSubmit)`** — React Hook Form intercepts the form submit event, runs Zod validation, and only calls `onSubmit` if all fields pass. Invalid fields populate `errors` instead.

**`{ token, ...data }`** — spreads the form data and adds the token from the URL. BE needs all four fields: `token`, `first_name`, `last_name`, `password`.

**`navigate(ROUTES.LOGIN)`** — programmatic navigation after successful registration. Uses the constant from `routes.ts`.

### Error handling pattern

```typescript
const code = err.response?.data?.error_code
setPageError(ERROR_MESSAGES[code] ?? 'Fallback message.')
```

`?.` is optional chaining — if `err.response` is undefined, the whole expression returns undefined instead of throwing. Safe to use on unknown error shapes.

`ERROR_MESSAGES[code]` looks up the user-facing message by error code. `?? 'Fallback'` provides a default if the code is not in the map.
