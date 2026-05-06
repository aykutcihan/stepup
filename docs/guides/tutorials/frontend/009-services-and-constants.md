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

All frontend page paths in one place.

```typescript
export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
}
```

Usage:
```typescript
navigate(ROUTES.LOGIN)
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

## src/services/

Service files contain the actual API calls. They use `axios`, the constants from above, and the types from `api.ts`.

```
src/services/
  authService.ts      ← login, logout, register, validateInvitation
  invitationService.ts ← create, list, resend (added when needed)
```

One file per domain — same grouping as BE routers.

---

## src/services/authService.ts Explained

```typescript
import axios from 'axios'
import type { components } from '@/types/api'
import { API } from '@/constants/apiEndpoints'

type InvitationValidateResponse = components['schemas']['InvitationValidateResponse']
type RegisterRequest = components['schemas']['RegisterRequest']
type UserResponse = components['schemas']['UserResponse']

export async function validateInvitation(token: string): Promise<InvitationValidateResponse> {
  const res = await axios.get(API.INVITATIONS.VALIDATE, { params: { token } })
  return res.data
}

export async function register(data: RegisterRequest): Promise<UserResponse> {
  const res = await axios.post(API.AUTH.REGISTER, data)
  return res.data
}
```

### `axios.get` with `params`

```typescript
axios.get(API.INVITATIONS.VALIDATE, { params: { token } })
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
