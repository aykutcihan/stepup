# Testing — Unit vs Integration

Testing is not just about making sure code works today. It is a guarantee that future changes will not silently break existing behavior.

---

## Two Types of Tests

### Unit Test

A unit test focuses on the **smallest piece of code** — usually a single function or method. It isolates that piece from everything else and checks whether the logic produces the expected output for a given input.

- **Goal:** Given this input, does the function return the expected output?
- **Isolation:** No database, no HTTP, no external service. If the function depends on something external, that dependency is replaced with a **Mock** (a fake object that pretends to be the real thing).
- **Speed:** Very fast. Thousands can run in seconds.

**When to write:**
Service layer logic, business rules, edge cases, error paths. Any time a condition, calculation, or decision is made in code.

---

### Integration Test

An integration test checks whether **multiple pieces work correctly together** — the endpoint, the service, the repository, and the database, all in one flow.

- **Goal:** When I send a request to this endpoint, is the correct data written to the database and is the correct JSON returned?
- **Isolation:** Not isolated. Uses a real FastAPI application, a real test database, and real HTTP requests via `TestClient`.
- **Speed:** Slower than unit tests because actual I/O (database) is involved.

**When to write:**
Endpoint contracts — happy paths, HTTP status codes, response body shape, database side effects.

---

## Comparison

| | Unit Test | Integration Test |
|--|-----------|-----------------|
| **Scope** | Single function or class | Full endpoint flow |
| **Dependencies** | None — mocked | Real test DB, real HTTP |
| **Speed** | Very fast | Slower |
| **Finds** | Logic bugs | Integration bugs (wrong column, type mismatch, missing FK) |

---

## Why You Need Both

**Without unit tests:** To catch a logic bug you have to spin up the whole system and fire an HTTP request every time. Slow and fragile.

**Without integration tests:** Your service layer can work perfectly in isolation but if a column name is wrong or a router parameter type does not match, you will never know until it hits production.

---

## Test Scenarios

Every function has three types of scenarios to consider:

**Happy path**
Everything goes right. The function receives valid input and returns the expected result.
```
valid token → invitation returned
```

**Sad path**
Expected failure scenarios — business rules that reject invalid input. These are not bugs, they are intentional behavior.
```
token not found      → NotFoundError
invitation expired   → ValidationError
invitation used      → ValidationError
```

**Edge case**
Boundary values and unexpected inputs — things that sit right at the limit of what the system handles.
```
token expires exactly at this millisecond
empty string passed as token
```

When writing tests, always cover the happy path first, then sad paths, then edge cases if the logic warrants it.

---

## Test Database

We do **not** use SQLite for integration tests even though it is simpler to set up. The reason: production runs on PostgreSQL. Different databases have different behaviors (constraints, type handling, query planner). Testing on SQLite would mask bugs that only appear on PostgreSQL.

Instead we use a dedicated `stepup_test` database inside the same PostgreSQL container. See [infra/005-test-infrastructure.md](../../infra/005-test-infrastructure.md) for setup details.

---

## In This Project

| Layer | Test type | Location |
|-------|-----------|----------|
| `app/services/` | Unit | `tests/unit/services/` |
| `app/api/v1/` | Integration | `tests/integration/api/` |
