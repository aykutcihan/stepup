# Alembic

## What is Alembic?

Alembic is a database migration tool for SQLAlchemy.
It tracks database schema changes over time — like Git, but for the database.

---

## The Problem Without Alembic

You create a `users` table. Later you need to add an `email` column.

Without Alembic:
```sql
-- manually run this on every environment
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

Problems:
- How does a new developer know what to run?
- What order do the changes go in?
- What if you need to undo a change?
- No record of who changed what

---

## How Alembic Works

```
1. You change a model (add column, new table, etc.)

2. Alembic compares:
   "What does the model say should exist?"
   vs
   "What actually exists in the database?"

3. Alembic writes a migration file with the difference

4. You run the migration → database is updated
```

It is the same concept as Git commits, but for database schema:

| Git | Alembic |
|---|---|
| `git commit` | `alembic revision` |
| `git push` | `alembic upgrade head` |
| `git log` | `alembic history` |
| `git revert` | `alembic downgrade` |

---

## Our File Structure

```
apps/backend/
  alembic.ini              ← Alembic configuration
  alembic/
    env.py                 ← how migrations connect to the database
    script.py.mako         ← template for new migration files
    versions/
      85ee24f36bec_create_users_table.py  ← our first migration
```

---

## alembic.ini Explained

```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+psycopg2://stepup:stepup123@db:5432/stepup_db
```

| Setting | Meaning |
|---|---|
| `script_location` | Where the alembic folder is |
| `sqlalchemy.url` | Database connection string for migrations |

### Why psycopg2 here and asyncpg in the app?

```
alembic.ini  → postgresql+psycopg2://...  (sync driver — Alembic needs sync)
.env         → postgresql+asyncpg://...   (async driver — FastAPI needs async)
```

Alembic runs migration scripts sequentially — sync is fine.
FastAPI handles many requests at once — async is required.

---

## alembic/env.py Explained

```python
from app.models.base import Base
from app.models.user import User  # noqa: F401

target_metadata = Base.metadata
```

This is the key part. `target_metadata = Base.metadata` tells Alembic:
"Compare the database against these models."

`from app.models.user import User` — why import if we don't use it directly?
When Python imports `User`, SQLAlchemy registers the `users` table in `Base.metadata`.
Without this import, Alembic would not know the `users` table should exist.

Every new model must be imported here, otherwise Alembic will not detect it.

---

## Migration File Anatomy

Our generated migration `85ee24f36bec_create_users_table.py`:

```python
revision = '85ee24f36bec'       # unique ID for this migration
down_revision = None            # no previous migration (this is the first one)

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), ...),
        sa.Column('updated_at', sa.DateTime(timezone=True), ...),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
```

`upgrade()` = apply the change (forward)
`downgrade()` = undo the change (backward)

Alembic generated this file automatically from our `User` model.
We did not write it manually.

---

## Commands

```powershell
# Generate a new migration (auto-detect model changes)
docker-compose run --rm backend alembic revision --autogenerate -m "description"

# Apply all pending migrations
docker-compose run --rm backend alembic upgrade head

# Roll back one migration
docker-compose run --rm backend alembic downgrade -1

# See migration history
docker-compose run --rm backend alembic history

# See current migration version
docker-compose run --rm backend alembic current
```

### When I used these

```
First migration:
  alembic revision --autogenerate -m "create users table"
  → Generated 85ee24f36bec_create_users_table.py

Applied to database:
  alembic upgrade head
  → Running upgrade -> 85ee24f36bec, create users table
  → users table created in stepup_db
```

---

## Workflow: Adding a New Column

When we add `role` to the `User` model later:

```python
# 1. Add to model
class User(Base, TimestampMixin):
    ...
    role: Mapped[str] = mapped_column(String(50), nullable=False)
```

```powershell
# 2. Generate migration
docker-compose run --rm backend alembic revision --autogenerate -m "add role to users"
# → Alembic detects the new column, writes migration file

# 3. Apply migration
docker-compose run --rm backend alembic upgrade head
# → Column added to database
```

Never modify the database manually. Always go through Alembic.

---

## alembic_version Table

When Alembic runs a migration, it records the revision ID in a special table:

```sql
SELECT * FROM alembic_version;
-- revision_num
-- 85ee24f36bec
```

This is how Alembic knows which migrations have already been applied
and which are still pending. Never delete or modify this table manually.