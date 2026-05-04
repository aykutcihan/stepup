# Enum Conventions

This guide defines how enums are organized and written in this project.

---

## Location

All enums live in a dedicated `app/enums/` package — separate from models.

```
app/enums/
    __init__.py       (empty)
    user_role.py      → UserRole
    task_status.py    → TaskStatus (added when needed)
    plan_status.py    → PlanStatus (added when needed)
```

---

## Rules

**One file per enum.** Each file contains exactly one enum class.

**Functional file names.** The file name describes what the enum represents,
not that it is an enum.

```
user_role.py      not enums.py
task_status.py    not statuses.py
```

**Why a separate package?** Multiple models can need the same enum.
Keeping enums in `app/enums/` prevents circular imports — models import from enums,
never the other way around.

---

## How to Write an Enum

```python
# app/enums/user_role.py

import enum


class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"
```

`str` mixin ensures the enum serializes to a plain string in JSON responses
and works correctly with SQLAlchemy string columns — no extra conversion needed.

---

## How to Use in a Model

```python
from sqlalchemy import Enum as SAEnum
from app.enums.user_role import UserRole

role: Mapped[UserRole] = mapped_column(
    SAEnum(UserRole, name="user_role"), nullable=False
)
```

`name="user_role"` sets the PostgreSQL TYPE name in snake_case.
All models using the same enum must reference the same `name`.

---

## How to Add a New Enum

1. Create `app/enums/<functional_name>.py`
2. Define the enum class with `str` mixin
3. Import it wherever needed (model, schema, service)

No changes needed to `app/enums/__init__.py` — it stays empty.
