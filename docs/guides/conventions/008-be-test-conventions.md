# Test Conventions

This guide covers how we structure, name, and write tests in this project.

---

## Directory Structure

```
apps/backend/tests/
├── conftest.py              ← shared fixtures for all tests
├── unit/
│   └── services/
│       └── test_<name>_service.py
└── integration/
    └── api/
        └── test_<name>_endpoints.py
```

---

## Unit vs Integration

| | Unit | Integration |
|--|------|-------------|
| **What it tests** | Service logic in isolation | Full request → response cycle |
| **Database** | No — repositories are mocked | Yes — real `stepup_test` DB |
| **HTTP** | No | Yes — FastAPI `TestClient` |
| **Speed** | Fast | Slower |
| **When to write** | Business rules, edge cases, error paths | Happy paths, endpoint contracts |

**Rule of thumb:** if the logic involves a condition, a calculation, or an error case — write a unit test. If the question is "does this endpoint return 200 with the right body?" — write an integration test.

---

## conftest.py

`tests/conftest.py` contains fixtures shared by all tests.

```python
test_engine     # SQLAlchemy engine connected to stepup_test
TestSessionLocal  # session factory for the test engine
```

### Fixtures

| Fixture | Scope | What it does |
|---------|-------|--------------|
| `setup_database` | session | Creates all tables before the test run, drops them after |
| `db_session` | function | Opens a DB session, rolls back after each test — keeps tests isolated |
| `client` | function | FastAPI async HTTP client with `get_db` overridden to use the test session |

**Why rollback instead of truncate?**
Rolling back the transaction after each test is faster than truncating tables. The DB never actually sees the committed data — it is as if the test never ran.

**Why override `get_db`?**
The `client` fixture replaces the real `get_db` dependency with one that yields the test session. This means the endpoint, service, and repository all operate on the same test transaction — so the rollback at the end cleans everything up.

---

## Branch Naming

```
test/be-us-001-invitation-service   ← backend tests for US-001
test/fe-us-001-invite-form          ← frontend tests for US-001
```

Pattern: `test/<be|fe>-us-<number>-<short-description>`

---

## Commit Convention

```
test(be-us-001): create unit tests for invitation service
test(be-us-001): add integration tests for invite endpoint
test(fe-us-001): add component tests for invite form
```

Scope always includes `be-` or `fe-` to distinguish backend from frontend in the monorepo commit history.

---

## File Naming

Test files mirror the file they test:

| Source file | Test file |
|-------------|-----------|
| `app/services/invitation_service.py` | `tests/unit/services/test_invitation_service.py` |
| `app/api/v1/invitation.py` | `tests/integration/api/test_invitation_endpoints.py` |

---

## Function Naming

Pattern: `test_<function_name>_<scenario>_<expected_outcome>`

Reading the function name should tell you exactly what is being tested and what the expected result is — no comment needed.

```python
# validate_invitation — 4 scenarios
test_validate_invitation_returns_invitation_when_token_is_valid
test_validate_invitation_raises_not_found_when_token_does_not_exist
test_validate_invitation_raises_error_when_invitation_is_expired
test_validate_invitation_raises_error_when_invitation_is_already_used

# create_invitation — scenarios
test_create_invitation_returns_invitation_when_email_is_new
test_create_invitation_raises_error_when_user_already_exists
```

**Rules:**
- Always start with `test_`
- All lowercase, words separated by underscores
- Include the function under test, the input condition, and the expected outcome
- Avoid vague names like `test_valid_case` or `test_error` — they say nothing

---

## Grouping Tests with Classes

Group test functions by the source function they test using a class. This keeps the file readable as it grows — you always know where to find tests for a specific function.

```python
class TestValidateInvitation:
    async def test_returns_invitation_when_token_is_valid(self, service, mock_db): ...
    async def test_raises_not_found_when_token_does_not_exist(self, service, mock_db): ...
    async def test_raises_error_when_invitation_is_expired(self, service, mock_db): ...
    async def test_raises_error_when_invitation_is_already_used(self, service, mock_db): ...


class TestCreateInvitation:
    async def test_returns_invitation_when_email_is_new(self, service, mock_db): ...
    async def test_raises_error_when_user_already_exists(self, service, mock_db): ...
```

One class per source function. pytest discovers and runs all methods starting with `test_` inside classes automatically — no extra configuration needed.

Note: class methods receive `self` as the first parameter, followed by fixtures.

**Common mistake:** forgetting `self` inside a class. Without it, pytest treats the first fixture as `self` — the test class instance — and the fixture is never injected.

---

## Common Pitfall: Expired SQLAlchemy Objects

After `db.commit()` or any HTTP request that triggers a commit, SQLAlchemy marks all ORM objects in the session as **expired**. Accessing any attribute on an expired object triggers a lazy load — which fails in async context with:

```
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called
```

### In test fixtures (between requests)

The `hr_admin_user` fixture is created once and reused across requests. After the first request commits, the object expires. The fix is to refresh it in `override_get_current_user`:

```python
async def override_get_current_user():
    await db_session.refresh(hr_admin_user)  # re-loads from DB after any commit
    return hr_admin_user
```

This is already applied in `tests/integration/api/conftest.py`.

### In test bodies (between requests)

If you create an ORM object in a test, then make an HTTP request (which commits), then try to read the object's attributes — it will be expired:

```python
# Wrong — dept.id accessed after a commit has expired the object
dept = Department(name="Engineering")
db_session.add(dept)
await db_session.flush()

await client.post("/api/v1/departments/", json={"name": "HR"})  # triggers commit

assert something == str(dept.id)  # MissingGreenlet crash
```

**Fix:** save primitive values immediately after `flush`, before any request:

```python
dept = Department(name="Engineering")
db_session.add(dept)
await db_session.flush()
dept_id = str(dept.id)  # save before any commit

await client.post("/api/v1/departments/", json={"name": "HR"})

assert something == dept_id  # safe — plain string, not an ORM attribute
```

**Rule:** never access ORM object attributes after a request. Save what you need as plain values (`str`, `uuid.UUID`, `int`) immediately after `flush`.

### In responses with nested relationships

When a service commits and then returns an ORM object that has a relationship
(e.g. `plan.tasks`), Pydantic's `model_validate` accesses the relationship
synchronously. If the session expired the object after commit, this triggers a
lazy load in a sync context — another `MissingGreenlet` crash.

The fix is `expire_on_commit=False` on the test session so objects are never
expired after a savepoint commit:

```python
# tests/conftest.py
session = AsyncSession(
    conn,
    join_transaction_mode="create_savepoint",
    expire_on_commit=False,   # prevents MissingGreenlet on relationship access
)
```

This is already set in `tests/conftest.py`. If you ever recreate or replace the
session fixture, make sure to include it — especially for any endpoint that
returns nested objects (e.g. a plan with its tasks).

```python
# Wrong — pytest treats `service` as `self`
async def test_something(service, mock_db): ...

# Correct
async def test_something(self, service, mock_db): ...
```

The error you will see: `AttributeError: 'TestXxx' object has no attribute '...'`
