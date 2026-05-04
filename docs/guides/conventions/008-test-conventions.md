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
