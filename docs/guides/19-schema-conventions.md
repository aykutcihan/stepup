# Schema Naming Conventions

This guide defines how Pydantic schemas are named and structured in this project.

---

## Suffix Rules

| Suffix | Purpose | When to use |
|--------|---------|-------------|
| `Base` | Shared fields between multiple schemas | Only when two or more schemas genuinely share fields |
| `Create` | POST request body | When creating a new resource |
| `Update` | PATCH request body | When partially updating a resource — all fields are `Optional` |
| `Response` | Data returned to the client | Every endpoint that returns data |
| `Request` | POST request body for actions | When the operation is an action, not a resource creation (e.g. login, register) |

---

## When to Use Base

Only introduce `Base` when there is real field sharing between schemas.
Do not add it by default.

**Use Base:**
```python
class InvitationBase(BaseModel):
    email: EmailStr
    role: UserRole

class InvitationCreate(InvitationBase):
    pass  # inherits email and role

class InvitationResponse(InvitationBase):
    id: uuid.UUID
    expires_at: datetime
```

**Skip Base** when schemas have different enough fields that sharing adds no value.

---

## Update Schemas

All fields in an `Update` schema are `Optional` — the client sends only what changed.

```python
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

---

## Create vs Response — Why Two Classes

`Create` and `Response` are always separate because the client and the server
control different fields.

| Who sets it | Where it lives |
|-------------|---------------|
| Client sends | `Create` — email, role |
| System generates | `Response` only — id, expires_at, created_at |

The client must never be able to supply `id` or `expires_at` directly.
Keeping them in separate schemas enforces this at the validation layer.

---

## Response Schemas

`Response` schemas define exactly what the client receives.
They should never expose internal fields like `password_hash` or `deleted_at`.

```python
class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### from_attributes=True

SQLAlchemy returns data as Python objects — you access fields with dot notation (`obj.email`).
Pydantic by default expects a dictionary (`obj["email"]`).

`from_attributes=True` tells Pydantic to read attributes using dot notation instead,
so it can consume a SQLAlchemy model instance directly.

Without it:
```python
# TypeError — Pydantic cannot read a SQLAlchemy object
return InvitationResponse(db_invitation)
```

With it:
```python
# Pydantic reads db_invitation.id, db_invitation.email, etc. automatically
return InvitationResponse.model_validate(db_invitation)
```

`model_validate()` is the method used to build a schema from a SQLAlchemy instance.
FastAPI also calls this automatically when you set `response_model=InvitationResponse`
on an endpoint.

---

## File Location

All schemas live under `app/schemas/`, one file per domain:

```
app/schemas/
    invitation.py   → InvitationCreate, InvitationResponse
    user.py         → UserCreate, UserUpdate, UserResponse
    token.py        → TokenResponse, RefreshTokenRequest
```

---

## Example — Invitation

```python
# app/schemas/invitation.py

class InvitationCreate(BaseModel):
    email: EmailStr
    role: UserRole

class InvitationResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
```
