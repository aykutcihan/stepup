# SQLAlchemy

## What is SQLAlchemy?

SQLAlchemy is a Python ORM (Object-Relational Mapper).
It lets you work with database tables as Python classes and objects,
instead of writing raw SQL.

---

## ORM vs Raw SQL

Without ORM (raw SQL):
```python
cursor.execute("""
    INSERT INTO users (id, email, password_hash, first_name, last_name)
    VALUES (%s, %s, %s, %s, %s)
""", (str(uuid4()), email, hash, first, last))
```

With SQLAlchemy ORM:
```python
user = User(email=email, password_hash=hash, first_name=first, last_name=last)
db.add(user)
await db.commit()
```

Same result, but the Python version is:
- Readable
- Type-safe (TypeScript-like type hints)
- Protected from SQL injection automatically
- Easier to test

---

## SQLAlchemy 2.0 — The Version We Use

We use SQLAlchemy 2.0 with the new "mapped column" style.
It adds full Python type hint support.

Old style (SQLAlchemy 1.x):
```python
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True)
```

New style (SQLAlchemy 2.0):
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

The new style gives you autocomplete and type checking in VS Code.

---

## base.py Explained

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
```

### Base class

```python
class Base(DeclarativeBase):
    pass
```

Every model inherits from `Base`. This tells SQLAlchemy:
"This class represents a database table."

Alembic reads `Base.metadata` to know which tables exist and generate migrations.

### TimestampMixin

Instead of adding `created_at`, `updated_at`, `deleted_at` to every model,
we define them once in `TimestampMixin` and mix them in:

```python
class User(Base, TimestampMixin):  # inherits from both
    __tablename__ = "users"
    id = ...
    # created_at, updated_at, deleted_at come automatically from TimestampMixin
```

| Column | Purpose |
|---|---|
| `created_at` | When the record was created. Set automatically by the database. |
| `updated_at` | When the record was last updated. Updated automatically on every save. |
| `deleted_at` | When the record was "deleted" (soft delete). NULL means active. |

### Soft Delete

Records are never truly deleted. Instead:
```python
user.deleted_at = datetime.now()  # "delete"
```

All queries filter by `WHERE deleted_at IS NULL` to show only active records.

Why soft delete?
- Audit trail stays intact — we can still see who approved what
- GDPR anonymization is possible — replace PII with "User [ID]" while keeping the record structure
- Accidental deletions can be recovered

---

## User Model Explained

```python
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
```

### UUID Primary Key

```python
id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
)
```

We use UUID instead of integer (1, 2, 3...) for security:

```
Integer IDs:  /api/v1/users/1 → /api/v1/users/2 → predictable, enumerable
UUID IDs:     /api/v1/users/a7f3c2d1-... → unpredictable, safe
```

`default=uuid.uuid4` — Python generates the UUID before inserting.
`as_uuid=True` — SQLAlchemy stores it as a native PostgreSQL UUID type.

### Email with Index

```python
email: Mapped[str] = mapped_column(
    String(255),
    unique=True,    # no two users can have the same email
    nullable=False, # required field
    index=True,     # fast lookup by email (used on every login)
)
```

`index=True` creates a database index. Without it:
```
Login query: SELECT * FROM users WHERE email = 'x@x.com'
→ scans every row (slow when many users)

With index:
→ jumps directly to the row (fast regardless of user count)
```

### Password Hash

```python
password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
```

Passwords are **never stored as plain text**.
The `auth_service` will hash the password with bcrypt before saving.
This column only stores the hash result.

```
User enters:    "mypassword123"
bcrypt hashes:  "$2b$12$xxxxx..."   ← this is stored
```

### YAGNI Applied

Current model has: `id`, `email`, `password_hash`, `first_name`, `last_name`.

Not yet added (will be added when the feature is implemented):
- `role` → when role/permission system is built
- `is_active` → when user deactivation is built
- `department_id` → when Department model is built
- `manager_id` → when manager relationship is built

---

## database.py Explained

```python
engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Why Async?

FastAPI is async. If we used a sync database driver, it would block the entire
application while waiting for a database response.

```
Sync:  Request 1 → wait for DB → respond → Request 2 (had to wait!)
Async: Request 1 → ask DB → while waiting → handle Request 2 → DB responds → respond to Request 1
```

### get_db() — Dependency Injection

`get_db()` is a FastAPI dependency. Every endpoint that needs the database
declares it as a parameter:

```python
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    # db session is ready to use
    result = await db.execute(select(User))
    return result.scalars().all()
```

FastAPI automatically:
1. Calls `get_db()` before the endpoint runs
2. Passes the session to the endpoint
3. Calls the rest of `get_db()` after the endpoint finishes (commit or rollback)

`yield` is the key — it pauses `get_db()`, gives the session to the endpoint,
and resumes after the endpoint returns.