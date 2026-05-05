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
