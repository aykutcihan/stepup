# Coding Conventions

This guide defines code style and naming decisions for this project.

---

## Comments and Docstrings

Do not add comments or docstrings by default.

A well-named function, method, or variable already describes what it does.
Only add a comment when the **why** is non-obvious — a hidden constraint, a workaround,
or behavior that would surprise a reader.

```python
# No — the name already says this
async def get_by_token(self, db, token):
    """Returns invitation by token."""  # unnecessary

# Yes — the why is not obvious
# token_urlsafe returns a URL-safe string, length ~43 chars for n=32
token = secrets.token_urlsafe(32)
```

---

## Method Naming

Use verb + noun pattern. The name must describe the action and the subject.

| Pattern | Example |
|---------|---------|
| `get_by_{field}` | `get_by_token`, `get_by_email` |
| `get_all_{resource}` | `get_all_invitations` |
| `create_{resource}` | `create_invitation` |
| `update_{resource}` | `update_user` |
| `delete_{resource}` | `delete_invitation` |
| `validate_{resource}` | `validate_invitation` |
| `mark_{resource}_{state}` | `mark_invitation_used` |
| `send_{action}` | `send_invitation_email` |

---

## Variable Naming

Use snake_case. Names must be descriptive — no single letters except loop counters.

```python
# No
u = db.get(User, id)
r = await inv_repo.create(db, inv)

# Yes
user = db.get(User, user_id)
invitation = await invitation_repository.create(db, invitation)
```

---

## Class Naming

Use PascalCase. Class name describes what it is, not what it does.

```python
InvitationRepository   # correct
InvitationRepositoryClass  # no — "Class" is redundant
ManageInvitations      # no — that's a method name, not a class name
```

---

## Transaction Management

Repositories do not commit. Services decide when to commit.

**Repository — only stages changes:**
```python
async def create(self, db: AsyncSession, user: User) -> User:
    db.add(user)
    return user
```

**Service — commits when all operations are ready:**
```python
db.add(user)
invitation.used_at = datetime.now(timezone.utc)
await db.commit()
await db.refresh(user)
```

**Why:** If a service performs two operations and each repository commits separately,
a failure between them leaves the database in an inconsistent state.
Committing once in the service ensures both operations succeed or neither does — atomicity.

Single-operation flows can commit in the repository. Multi-operation flows must
commit in the service.

---

## Constants

No magic numbers or strings. All constants go in the relevant module or `app/core/constants.py`.

```python
# No
expires_at = datetime.now(timezone.utc) + timedelta(days=7)

# Yes
INVITATION_EXPIRY_DAYS = 7
expires_at = datetime.now(timezone.utc) + timedelta(days=INVITATION_EXPIRY_DAYS)
```
