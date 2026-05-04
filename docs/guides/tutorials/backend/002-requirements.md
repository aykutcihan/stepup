# requirements.txt & pyproject.toml

## What is requirements.txt?

A plain text file listing all Python packages the project needs.
One package per line. pip reads this file and installs everything.

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.36
...
```

---

## Our requirements.txt Explained

### Web Framework
```
fastapi==0.115.0          # the API framework
uvicorn[standard]==0.30.0 # the server that runs FastAPI
                          # [standard] adds extra speed tools: uvloop, httptools
```

### Database
```
sqlalchemy==2.0.36        # ORM — Python objects ↔ database tables
alembic==1.13.3           # database migrations
asyncpg==0.29.0           # async PostgreSQL driver (used by the app at runtime)
psycopg2-binary==2.9.9    # sync PostgreSQL driver (used by Alembic for migrations)
```

### Why Two PostgreSQL Drivers?

This is important to understand:

| Driver | Type | Used by | Why |
|---|---|---|---|
| `asyncpg` | Async | FastAPI app at runtime | FastAPI is async — needs async DB driver |
| `psycopg2-binary` | Sync | Alembic migrations | Alembic uses sync connections |

```
FastAPI app  → asyncpg  → async, handles many requests simultaneously
Alembic      → psycopg2 → sync, runs once, generates migration files
```

If we only had `asyncpg`, Alembic would fail with `ModuleNotFoundError: No module named 'psycopg2'`.
We discovered this when running our first migration — added `psycopg2-binary` to fix it.

### Validation & Settings
```
pydantic==2.9.2           # data validation (input/output schemas)
pydantic-settings==2.5.2  # reads .env file into Settings class
```

### Authentication
```
python-jose[cryptography]==3.3.0  # JWT token creation and verification
passlib[bcrypt]==1.7.4            # password hashing with bcrypt
python-multipart==0.0.12          # required for form data (login forms)
```

### Security
```
slowapi==0.1.9            # rate limiting (max N requests per minute)
```

### Cloud & Email
```
google-cloud-secret-manager==2.21.0  # read secrets from GCP Secret Manager
sendgrid==6.11.0                     # send emails via SendGrid
```

### Scheduling
```
apscheduler==3.10.4       # run scheduled jobs (deadline checks, reminders)
```

### Testing
```
pytest==8.3.3             # test runner
httpx==0.27.2             # async HTTP client for testing API endpoints
pytest-asyncio==0.24.0    # run async test functions with pytest
```

---

## Version Pinning

All packages use exact versions (`==`), not ranges (`>=`).

```
fastapi==0.115.0   ← exact version, always installs this
fastapi>=0.115.0   ← could install 0.120.0 in the future, might break things
```

Exact versions ensure the project builds identically on every machine and in every CI run.
"It works on my machine" problems disappear.

---

## What is pyproject.toml?

Configuration file for Python tools in the project.
Not for installing packages — for configuring how tools behave.

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]

[tool.ruff.isort]
known-first-party = ["app"]
```

### pytest configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"   # run async test functions automatically (no extra decorator needed)
testpaths = ["tests"]   # look for tests only in the tests/ folder
```

### ruff configuration

Ruff is our linter — checks code for errors and style issues.

```toml
[tool.ruff]
line-length = 88      # maximum line length (same as Black formatter)
select = ["E", "F", "I"]
```

| Rule set | What it checks |
|---|---|
| `E` | PEP8 style errors |
| `F` | Pyflakes — unused imports, undefined variables |
| `I` | Import sorting |

```toml
[tool.ruff.isort]
known-first-party = ["app"]   # treat "app" as our own code, not a third-party library
```

This tells ruff that `from app.models.user import User` is a local import,
so it sorts it separately from third-party imports like `from fastapi import FastAPI`.