# Post-mortem: User Registration 500 — Async Lazy-Load in Pydantic Validator

**Date:** 2026-05-17
**Branch:** `feature/email-template-service`
**Severity:** High — user registration always 500 when department was assigned
**Outcome:** Added `selectinload(User.department)` after commit in `register_user_from_invitation`

---

## Initial State

`register_user_from_invitation` created the user, committed the transaction, refreshed the ORM object, and returned it:

```python
user = User(
    email=invitation.email,
    role=invitation.role,
    first_name=first_name,
    last_name=last_name,
    password_hash=pwd_context.hash(password),
    department_id=invitation.department_id,
)
db.add(user)
invitation.used_at = datetime.now(UTC)
await db.flush()
await audit_service.log(...)
await db.commit()
await db.refresh(user)
return user
```

The `auth.py` register endpoint then serialized the user:

```python
return UserResponse.model_validate(user)
```

`UserResponse` includes a `department_name` field backed by a property on the `User` model:

```python
@property
def department_name(self) -> str | None:
    return self.department.name if self.department else None
```

---

## The Bug

`await db.refresh(user)` refreshes scalar columns but does **not** load relationship attributes. After refresh, `user.department` is in a lazy-load state.

When Pydantic's `model_validate` accesses `user.department_name`, the property accesses `self.department`. SQLAlchemy tries to lazy-load the relationship — but lazy loading requires a synchronous database call, which is not possible inside an `async` context. This raises `MissingGreenlet`:

```
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called;
can't call await from handler
```

Pydantic catches this exception and wraps it as a `ValidationError`, which FastAPI's unhandled exception middleware turns into a **500 Internal Server Error**.

The bug only triggered when the invitation had a `department_id` set. When `department_id` was `None`, `self.department` evaluated to `None` without triggering a load, and `department_name` returned `None` safely.

---

## Root Cause

`db.refresh(user)` does not eager-load relationships. After refresh, the `department` relationship is in a lazy-load pending state. In async SQLAlchemy, accessing a lazy-loaded relationship outside of an `await` context (e.g. from a synchronous property or Pydantic's attribute access) raises `MissingGreenlet`.

This pattern works fine in synchronous SQLAlchemy but fails silently in async contexts — the relationship just doesn't load instead of raising, until Pydantic tries to access it synchronously.

---

## Fix

Replace `db.refresh(user)` with an explicit `select` that eager-loads the `department` relationship:

```python
# Before
await db.commit()
await db.refresh(user)
return user

# After
await db.commit()
result = await db.execute(
    select(User)
    .where(User.id == user.id)
    .options(selectinload(User.department))
)
return result.scalar_one()
```

---

## Lessons Learned

1. **`db.refresh()` does not load relationships.** After a commit/refresh cycle, any relationship attribute is lazy — do not access it outside of an `await` context. If the caller needs relationship data, use `selectinload` in an explicit query.

2. **Lazy-load failures in async SQLAlchemy are `MissingGreenlet`, not `AttributeError`.** The error is raised at access time (property access, Pydantic serialization) rather than at query time. This makes it easy to miss in testing if tests do not assert on nested relationship fields.

3. **Pydantic `model_validate` accesses all declared fields synchronously.** Any field backed by a lazy-loaded relationship will trigger a `MissingGreenlet`. Always ensure relationships needed for serialization are loaded before calling `model_validate`.

4. **Test with non-null foreign keys.** This bug was invisible when `department_id` was `None`. Integration tests for registration should include a case where the invitation carries a valid `department_id`.
