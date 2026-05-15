# openapi-typescript — API Type Generation

## The Problem

FastAPI uses Python type hints (Pydantic models) to define request and response shapes. The frontend uses TypeScript types. These two are completely separate — if BE changes a schema, FE has no way of knowing unless types are manually kept in sync.

Manually writing TypeScript types that mirror Python schemas creates two problems:
- Duplication — the same shape defined in two places
- Drift — BE changes, FE types are forgotten, bugs appear at runtime

---

## The Solution

FastAPI automatically generates an OpenAPI specification at `/openapi.json`. This JSON file describes every endpoint, every request body, every response shape, and every enum in the entire API.

`openapi-typescript` reads this file and generates a TypeScript type file from it.

```
FastAPI → /openapi.json → openapi-typescript → src/types/api.ts
```

One command, always in sync.

---

## What Gets Generated

Everything in `src/types/api.ts`:

- **Schemas** — all Pydantic models (`RegisterRequest`, `UserResponse`, `InvitationValidateResponse`, etc.)
- **Enums** — all Python enums (`UserRole`)
- **Paths** — all endpoint paths with their request/response types

---

## How to Use Generated Types

```typescript
import type { components } from '@/types/api'

type InvitationValidateResponse = components['schemas']['InvitationValidateResponse']
type RegisterRequest = components['schemas']['RegisterRequest']
type UserRole = components['schemas']['UserRole']
```

The schema names match the Python class names exactly:

```
Python:     class InvitationValidateResponse(BaseModel): ...
TypeScript: components['schemas']['InvitationValidateResponse']
```

---

## Finding the Right Type Name

Two ways:

**1. Swagger UI** — open `http://localhost:8000/docs`, find the endpoint, look at the schema name in the response section.

**2. Search in api.ts** — `Ctrl+F` in `src/types/api.ts`, search for the Python class name.

---

## When to Regenerate

Run the generate command whenever BE schemas or endpoints change. Backend must be running (`docker compose up`):

```powershell
pnpm --filter frontend exec openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts
```

The `generate-types` script in `package.json` uses `http://backend:8000` which only works inside Docker network. Use `localhost:8000` when running from the host terminal.

**When to run:**
- After a new Pydantic model is added
- After a field is added, removed, or renamed in an existing schema
- After a new endpoint is added
- After an enum value is added or removed

The generated `src/types/api.ts` is committed to the repository — every developer has the same types without running the command themselves.

---

## When the Backend Is Not Running — Manual Update

If the backend cannot start (e.g. a broken Docker image, missing env vars, infrastructure outage), the generate command is unavailable. In that case, add the new fields directly to `src/types/api.ts` by hand and commit them. The file is just TypeScript — it can be edited like any other source file.

Find the schema by name (`Ctrl+F` for the Python class name) and add the missing fields:

```typescript
// Before — backend schema added return_comment but types weren't regenerated
OnboardingPlanTaskResponse: {
    id: string;
    title: string;
    // ...
};

// After — manually added
OnboardingPlanTaskResponse: {
    id: string;
    title: string;
    // ...
    return_comment: string | null;
    attachments: components["schemas"]["TaskAttachmentResponse"][];
    comments: components["schemas"]["TaskCommentResponse"][];
};
```

Once the backend is running again, regenerate with the command above and commit the result. The manual edit and the generated output should be identical — if they differ, the generate command wins.

---

## What NOT to Do

Do not write manual TypeScript types that mirror BE schemas:

```typescript
// ❌ Don't do this — duplicates what api.ts already has
type InvitationValidateResponse = {
  email: string
  role: string
}

// ✅ Do this
import type { components } from '@/types/api'
type InvitationValidateResponse = components['schemas']['InvitationValidateResponse']
```

---

## api.ts Size

`api.ts` grows as the API grows. This is expected and not a problem:
- The file is generated, not maintained by hand
- Only imported types end up in the production bundle (tree-shaking)
- The file is the single source of truth for all API types

---

## Two Types of Errors — What Goes Where

When the BE returns an error, there are two completely different kinds. Understanding this determines where the FE handles them.

### Type 1: Validation Errors (HTTPValidationError)

Produced automatically by FastAPI + Pydantic. The request is rejected at the door — before any business logic runs.

**When it happens:** A required field is missing, an email field has no `@`, a string is sent where a number is expected.

**HTTP status:** `422 Unprocessable Entity`

**Response shape:**
```json
{
  "detail": [
    { "msg": "field required", "loc": ["body", "password"] }
  ]
}
```

**Where it lives:** Already in `api.ts` as `HTTPValidationError` — generated automatically.

**Example in BE:**
```python
class RegisterRequest(BaseModel):
    token: str
    first_name: str
    last_name: str
    password: str   # If this is missing → 422, no code needed
```

---

### Type 2: Business Logic Errors (Custom Errors)

Produced manually by the developer. The request passes validation but fails a business rule — checked inside the service after hitting the database.

**When it happens:** Token expired, invitation already used, user already exists, wrong password.

**HTTP status:** `400 Bad Request` or `404 Not Found`

**Response shape:**
```json
{
  "success": false,
  "error_code": "INVITATION_EXPIRED",
  "message": "Invitation token has expired"
}
```

**Where it lives:** NOT in `api.ts` — FastAPI cannot auto-document these. They live in `src/constants/errorMessages.ts`.

**Example in BE:**
```python
# app/errors/messages.py — written by the developer
INVITATION_EXPIRED = ("INVITATION_EXPIRED", "Invitation token has expired")
INVITATION_ALREADY_USED = ("INVITATION_ALREADY_USED", "Invitation has already been used")
```

---

### Summary

| | Type 1: Validation | Type 2: Business Logic |
|---|---|---|
| Who produces it | FastAPI + Pydantic (automatic) | Developer (manual) |
| When | Before logic runs | Inside service, after DB check |
| HTTP status | 422 | 400 / 404 |
| In api.ts? | ✅ Yes (HTTPValidationError) | ❌ No |
| FE handles via | api.ts type | errorMessages.ts map |

See `009-services-and-constants.md` for how `errorMessages.ts` is structured and used.
