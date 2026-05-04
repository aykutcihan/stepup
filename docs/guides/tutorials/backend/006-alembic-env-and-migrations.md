# Alembic — env.py and Migration Workflow

This guide covers how Alembic connects Python models to the database
and how the `env.py` file controls that process.

---

## Core Concepts

| Concept | Role |
|---------|------|
| **Model** | Python class that defines the table structure |
| **Alembic** | Tool that reads models and translates changes into database operations |
| **Migration file** | Step-by-step instructions for a schema change (add column, create table, etc.) |
| **Database** | Where the changes are physically applied |

---

## How Alembic Discovers Models

Alembic compares `Base.metadata` (what your models say) against the live database
to detect what changed. For a model to appear in `Base.metadata`, it must be imported
before Alembic reads the metadata.

### Pattern used in this project

All models are registered in `app/models/__init__.py`:

```python
# app/models/__init__.py
from app.models.user import User  # noqa: F401
from app.models.invitation import Invitation  # noqa: F401
```

`env.py` imports the entire module in one line:

```python
# alembic/env.py
import app.models  # noqa: F401
```

This triggers `__init__.py`, which registers all models into `Base.metadata`.

**Why this pattern:** When you add a new model, you only update `app/models/__init__.py`.
You never need to touch `env.py` again.

---

## env.py — Two Modes

### Offline Mode

Generates a SQL script without connecting to the database.

```python
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
```

- `literal_binds=True` writes actual values into the SQL file instead of placeholders
- Useful when database access is restricted or when a DBA needs to review SQL before applying
- Generate the script: `alembic upgrade head --sql > migration.sql`

### Online Mode

Connects to the database and applies changes directly.

```python
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```

- `pool.NullPool` closes the connection immediately after migrations finish — no idle connections left open
- Used in CI/CD pipelines (GitHub Actions, GCP Cloud Build) for automatic deployment

---

## Key Parameters

| Parameter | What it does |
|-----------|-------------|
| `target_metadata = Base.metadata` | Tells Alembic which model definitions to compare against the database |
| `engine_from_config` | Reads the database URL from `alembic.ini` and creates the connection |
| `context.begin_transaction()` | Wraps all changes in a single transaction — if anything fails, nothing is applied |

---

## Database URL and Secrets

The database URL must never be hardcoded. In this project:

- **Local:** URL is set in `alembic.ini`, pointing to the Docker PostgreSQL container
- **Production:** URL is pulled from GCP Secret Manager via an environment variable

```python
import os
url = os.getenv("DATABASE_URL")
```

This switch is made when GCP Cloud SQL is connected — `alembic.ini` is updated or
the environment variable is injected by the CI/CD pipeline.

---

## Migration Workflow

```
1. Update the model         → add/change a field in app/models/
2. Register the model       → add import to app/models/__init__.py
3. Generate migration file  → alembic revision --autogenerate -m "description"
4. Review the file          → check alembic/versions/ — verify the generated SQL
5. Apply to database        → alembic upgrade head
```
