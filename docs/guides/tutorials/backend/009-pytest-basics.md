# pytest Basics

Core mechanics needed before writing tests.

---

## Fixtures

A fixture is a function that prepares something a test needs — a database session, an HTTP client, a mock object. pytest injects it automatically when a test function declares it as a parameter.

```python
@pytest.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
```

A test uses it by naming it as a parameter:

```python
async def test_something(db_session):
    # db_session is ready to use here
    ...
```

No need to call it manually — pytest sees the parameter name, finds the matching fixture, runs it, and passes the result in.

### `yield` in fixtures

When a fixture uses `yield`, everything before `yield` is setup, everything after is teardown. In `db_session` above, the rollback runs after every test automatically.

### `scope`

Controls how often the fixture runs:

| Scope | Runs |
|-------|------|
| `function` (default) | Once per test — fresh state every time |
| `session` | Once for the entire test run |

We use `scope="session"` for `setup_database` (create tables once) and function scope for `db_session` (rollback after each test).

---

## assert

`assert` is how a test checks its expectation. If the expression is `False`, the test fails.

```python
assert result == "expected"       # value equality
assert result is not None         # not null
assert len(items) == 3            # length check
assert "token" in response.json() # key exists in dict
assert response.status_code == 201
```

pytest rewrites `assert` statements to show the actual vs expected values on failure — no need for a special assertion library.

---

## MagicMock

Used in unit tests to replace real dependencies (repositories, external services) with fake objects that return controlled values.

```python
from unittest.mock import MagicMock, AsyncMock

mock_repo = MagicMock()
mock_repo.get_by_email = AsyncMock(return_value=None)
```

`AsyncMock` is for async functions — `await mock_repo.get_by_email(...)` will return `None` without touching the database.

You control what it returns, so you can test every code path (user found, user not found, exception raised) without a real database.

---

## Test Function Naming

```python
async def test_create_invitation_returns_token():
    ...

async def test_create_invitation_raises_if_email_already_invited():
    ...
```

Pattern: `test_<what>_<expected outcome>` — readable as a sentence.
