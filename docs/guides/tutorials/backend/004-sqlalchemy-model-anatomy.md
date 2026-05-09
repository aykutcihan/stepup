# SQLAlchemy Model Anatomy

This guide covers how database models are structured in this project,
using the `Invitation` model as a reference example.

---

## Model Structure

```python
class Invitation(Base, TimestampMixin):
    __tablename__ = "invitations"
```

`Invitation` inherits from two parents:

| Parent | What it provides |
|--------|-----------------|
| `Base` | Registers the class as a SQLAlchemy ORM model |
| `TimestampMixin` | Adds `created_at`, `updated_at`, `deleted_at` to every model automatically |

---

## Column Definitions

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid.UUID` | Primary key. Auto-generated with `uuid4` — unpredictable, safe to expose in URLs |
| `email` | `String(255)` | Email of the person being invited. `nullable=False` means it is required |
| `role` | `Enum` | Constrained to allowed values only (`employee`, `manager`, `hr_admin`) |
| `token` | `String(64)` | Unique invitation key used in the registration link. `unique=True` enforced at DB level |
| `invited_by` | `ForeignKey("users.id")` | Links back to the user who sent the invite |
| `expires_at` | `DateTime(timezone=True)` | Token expiry time. Set by the service layer when the invite is created |
| `used_at` | `datetime \| None` | `None` until the invited person completes registration. Then stamped with the timestamp |

---

## Key Concepts

### UUID vs Integer ID

Sequential IDs (1, 2, 3) let anyone guess valid resource identifiers.
UUIDs are random — impossible to enumerate. Used on all models in this project.

### Nullable vs Optional

`datetime | None` means the absence of a value is a valid state, not an error.
`used_at` starts as `None` (not yet used) and gets filled when registration completes.
`nullable=False` means the column must always have a value — the DB rejects a row without it.

### Enum

Prevents arbitrary strings from being stored in role or status columns.
SQLAlchemy creates a native PostgreSQL TYPE for it:

```sql
CREATE TYPE user_role AS ENUM ('employee', 'manager', 'hr_admin');
```

`name="user_role"` sets the name of that type in the database.
All models that use the same enum must reference the same `name`.

### Timezone-Aware Datetimes

`DateTime(timezone=True)` stores timestamps in UTC.
Always use this for any datetime column — avoids timezone bugs when the app runs across regions.

### TimestampMixin

Every model in this project uses `TimestampMixin`. It adds three columns automatically:

| Column | Purpose |
|--------|---------|
| `created_at` | When the row was inserted |
| `updated_at` | When the row was last modified |
| `deleted_at` | Soft delete — `None` means active, a timestamp means deleted |

Soft delete means rows are never physically removed. Queries filter `deleted_at IS NULL`.

---

## Relationships

SQLAlchemy `relationship()` links two models at the ORM level. When two models reference each other, a naive import causes a **circular import** — `user.py` imports `department.py`, `department.py` imports `user.py`, Python crashes.

### Solution: `TYPE_CHECKING`

```python
# department.py
from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User  # only imported by type checkers, not at runtime


class Department(Base, TimestampMixin):
    users: Mapped[list["User"]] = relationship("User", back_populates="department")
```

```python
# user.py
from app.models.department import Department  # safe — Department doesn't import User at runtime


class User(Base, TimestampMixin):
    department: Mapped["Department"] = relationship("Department", back_populates="users")
```

| Detail | Why |
|--------|-----|
| `TYPE_CHECKING` is `False` at runtime | The import inside the block never executes — no circular import |
| `TYPE_CHECKING` is `True` for Pylance/mypy | They see the import and resolve `"User"` as a real type — no IDE warning |
| `from __future__ import annotations` | Makes all annotations lazy strings by default — required when using `TYPE_CHECKING` imports in annotations |
| String reference `"User"` in `relationship()` | SQLAlchemy resolves it lazily after all models are loaded — does not need a live import |

### `back_populates` Rule

Both sides of a relationship must declare `back_populates` pointing to each other's attribute name.

```
Department.users  ←→  User.department
```

If the names don't match, SQLAlchemy raises a configuration error at startup.

---

## Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| Class names | PascalCase | `Invitation`, `UserRole` |
| Table names | snake_case | `invitations`, `plan_tasks` |
| Column names | snake_case | `invited_by`, `expires_at` |
| Enum type names (DB) | snake_case | `user_role`, `task_status` |
