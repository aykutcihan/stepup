# Test Infrastructure

This guide covers the test infrastructure setup: what tools we use, how the test database is configured, and how to run tests inside Docker.

---

## pyproject.toml

`pyproject.toml` is the standard Python project configuration file. We use it to configure two tools: `pytest` and `ruff`.

It lives at `apps/backend/pyproject.toml`.

### pytest configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
```

| Setting | What it does |
|---------|--------------|
| `asyncio_mode = "auto"` | Automatically treats async test functions as async — no need to add `@pytest.mark.asyncio` on every test |
| `asyncio_default_fixture_loop_scope = "function"` | Each test gets its own event loop — tests stay isolated from each other |
| `testpaths = ["tests"]` | Tells pytest where to look for tests — avoids scanning the entire project |

### ruff configuration

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

Ruff is a fast Python linter. `E` = style errors, `F` = logical errors, `I` = import ordering.

---

## Test Database

We use a separate `stepup_test` database inside the same `stepup-db` PostgreSQL container. This keeps test data completely isolated from development data.

**Why the same container instead of a separate one?**
A separate container adds complexity and resource usage without meaningful benefit at this stage. One container, two databases is the right tradeoff here.

### How it was created

```powershell
docker exec stepup-db psql -U stepup -d stepup_db -c "CREATE DATABASE stepup_test;"
```

Note: we connect via `-d stepup_db` because PostgreSQL requires an existing database to connect through — `stepup` does not exist as a database, only as a user.

### Connection string

Inside Docker containers, the database host is `db` (the service name in `docker-compose.yml`), not `localhost`.

```
TEST_DATABASE_URL=postgresql+asyncpg://stepup:stepup123@db:5432/stepup_test
```

This is different from `DATABASE_URL` only in the database name (`stepup_test` vs `stepup_db`).

### How it connects to the backend

`docker-compose.yml` passes `TEST_DATABASE_URL` to the backend container:

```yaml
environment:
  DATABASE_URL: ${DATABASE_URL}
  TEST_DATABASE_URL: ${TEST_DATABASE_URL}
```

`pydantic-settings` reads it into `Settings.TEST_DATABASE_URL`. `conftest.py` uses it to create the test engine.

---

## Running Tests

Tests run inside the `stepup-backend` container — the same environment as the application.

```powershell
docker exec stepup-backend python -m pytest --tb=short -q
```

| Flag | What it does |
|------|--------------|
| `--tb=short` | Shows a compact traceback on failure — easier to read than the default |
| `-q` | Quiet mode — hides individual test names, shows only the summary |

To run only unit tests:

```powershell
docker exec stepup-backend python -m pytest tests/unit --tb=short -q
```

To run only integration tests:

```powershell
docker exec stepup-backend python -m pytest tests/integration --tb=short -q
```
