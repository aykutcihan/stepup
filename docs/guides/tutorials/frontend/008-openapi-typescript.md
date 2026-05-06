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

Run the generate command whenever BE schemas or endpoints change:

```powershell
docker-compose run --rm frontend node_modules/.bin/openapi-typescript http://backend:8000/openapi.json -o src/types/api.ts
```

Or use the npm script shorthand (all services must be running):

```powershell
docker-compose run --rm frontend npm run generate-types
```

**When to run:**
- After a new Pydantic model is added
- After a field is added, removed, or renamed in an existing schema
- After a new endpoint is added
- After an enum value is added or removed

The generated `src/types/api.ts` is committed to the repository — every developer has the same types without running the command themselves.

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
