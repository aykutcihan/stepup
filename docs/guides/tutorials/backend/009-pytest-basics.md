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

**Mixing sync and async on the same object:**
`AsyncMock()` makes all attributes async by default. If the real object has some sync methods (like `db.add()` in SQLAlchemy — no `await`), override them explicitly in the fixture:

```python
@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()  # sync — SQLAlchemy's add() is not awaited
    return db
```

If you forget this, pytest will warn: `RuntimeWarning: coroutine was never awaited`.

You control what it returns, so you can test every code path (user found, user not found, exception raised) without a real database.

### autospec=True — protecting against typos and wrong signatures

By default, `MagicMock` silently accepts any attribute name — even ones that do not exist on the real class. This means a test can pass while referencing a method that does not exist in production.

`autospec=True` fixes this. It introspects the real class automatically and enforces both **attribute names** and **method signatures**.

```python
# Without autospec — dangerous
with patch("app.services.invitation_service.invitation_repository") as mock_repo:
    mock_repo.get_by_tokne = AsyncMock(...)  # typo — test still passes!

# With autospec=True — safe
with patch(
    "app.services.invitation_service.invitation_repository",
    autospec=True,
) as mock_repo:
    mock_repo.get_by_tokne = AsyncMock(...)  # AttributeError — typo caught immediately
    mock_repo.get_by_token()                 # TypeError — missing required arguments
```

**Why `autospec=True` over `spec=RealClass`:**
- `spec=RealClass` checks attribute names only
- `autospec=True` checks attribute names **and** method signatures — wrong number of arguments raises `TypeError`
- `autospec=True` does not require importing the real class — it introspects automatically

Always use `autospec=True` when patching.

---

## Test Function Naming

```python
async def test_create_invitation_returns_token():
    ...

async def test_create_invitation_raises_if_email_already_invited():
    ...
```

Pattern: `test_<what>_<expected outcome>` — readable as a sentence.

---

## Putting It Together — Behind the Scenes

Here is what actually happens when a unit test runs, using a real example from this project.

```python
@pytest.fixture
def service():
    return InvitationService()

@pytest.fixture
def mock_db():
    return MagicMock()

async def test_validate_invitation_returns_invitation_when_token_is_valid(
    service, mock_db
):
    mock_invitation = MagicMock()
    mock_invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    mock_invitation.used_at = None

    with patch("app.services.invitation_service.invitation_repository") as mock_repo:
        mock_repo.get_by_token = AsyncMock(return_value=mock_invitation)

        result = await service.validate_invitation(mock_db, "valid-token")

        assert result == mock_invitation
```

**Step 1 — Fixtures are injected**
pytest sees `service` and `mock_db` as parameters and runs those fixtures before the test. `service` gives a fresh `InvitationService()`. `mock_db` gives a `MagicMock()` — a fake database session that satisfies the type signature but does nothing.

**Step 2 — The stand-in invitation is built**
`mock_invitation` simulates a row that came back from the database: valid expiry (1 day from now), not yet used (`used_at = None`).

**Step 3 — `patch` swaps the real repository**
`invitation_service.py` has a module-level `invitation_repository` object. `patch` temporarily replaces it with `mock_repo` for the duration of the `with` block. When the block ends, the original is restored — other tests are not affected.

**Step 4 — `AsyncMock` controls the return value**
`get_by_token` is an async function (called with `await`). `AsyncMock(return_value=mock_invitation)` tells it: "when called, do not go to the database — return this object instead."

**Step 5 — The service runs for real**
`validate_invitation` executes normally. It calls `get_by_token` (gets `mock_invitation`), checks `expires_at` (valid), checks `used_at` (None) — all conditions pass, it returns the invitation.

**Step 6 — assert**
The test confirms the returned object is exactly the one we prepared. If any step above had gone wrong, the assert would fail and pytest would show the difference.

The entire test runs in memory. No database was touched.
