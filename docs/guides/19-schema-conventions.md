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

`from_attributes=True` allows the schema to be built directly from a SQLAlchemy model instance.

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
