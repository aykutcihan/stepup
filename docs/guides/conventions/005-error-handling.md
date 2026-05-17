# Error Handling

This guide explains how errors are structured, raised, and returned to the client in this project.

---

## Package Structure

```
app/errors/
    __init__.py    ← exception classes
    messages.py    ← error code and message constants
    handlers.py    ← FastAPI exception handlers
```

---

## How It Works

```
Service raises exception
        ↓
Handler catches it
        ↓
JSON response returned to client
```

---

## 1. Exception Classes — `__init__.py`

All custom exceptions inherit from `BaseAppError`.

```python
class BaseAppError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

class NotFoundError(BaseAppError):
    pass

class ValidationError(BaseAppError):
    pass
```

Every exception carries two pieces of information:
- `code` — machine-readable identifier for the frontend
- `message` — human-readable description for logging and debugging

Import: `from app.errors import NotFoundError, ValidationError`

---

## 2. Error Messages — `messages.py`

All error codes and messages are defined as tuples in one place.

```python
# Invitation
INVITATION_NOT_FOUND = ("INVITATION_NOT_FOUND", "Invitation not found")
INVITATION_EXPIRED = ("INVITATION_EXPIRED", "Invitation token has expired")
INVITATION_ALREADY_USED = ("INVITATION_ALREADY_USED", "Invitation has already been used")

# User
USER_ALREADY_EXISTS = ("USER_ALREADY_EXISTS", "A user with this email already exists")
```

Usage in service:

```python
from app.errors import messages

raise NotFoundError(*messages.INVITATION_NOT_FOUND)
# expands to: raise NotFoundError("INVITATION_NOT_FOUND", "Invitation not found")
```

The `messages.` prefix makes the source immediately visible at the call site.

---

## 3. Handlers — `handlers.py`

Handlers catch exceptions and convert them to HTTP responses.

```python
@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "error_code": exc.code, "message": exc.message},
    )
```

Registered in `main.py`:

```python
from app.errors.handlers import register_error_handlers
register_error_handlers(app)
```

---

## Response Format

Every error response follows this structure:

```json
{
  "success": false,
  "error_code": "INVITATION_NOT_FOUND",
  "message": "Invitation not found"
}
```

| Field | Purpose |
|-------|---------|
| `success` | Always `false` on error — frontend can check this |
| `error_code` | Machine-readable code — frontend maps this to a localized message |
| `message` | Human-readable — for logging and debugging, not shown to end users |

---

## HTTP Status Codes

| Exception | Status Code |
|-----------|------------|
| `NotFoundError` | 404 |
| `ValidationError` | 400 |

---

## Adding a New Error

1. Add the message tuple to `messages.py` under the relevant domain section
2. Raise with `raise NotFoundError(*messages.YOUR_NEW_ERROR)` in the service
3. If a new exception class is needed, add it to `__init__.py` and register a handler in `handlers.py`
4. Add the error code to the frontend `ERROR_MESSAGES` map (see Frontend section below)

---

## Frontend Error Handling

### `ERROR_MESSAGES` map — `src/constants/errorMessages.ts`

The frontend maps backend `error_code` values to user-facing strings:

```ts
export const ERROR_MESSAGES: Record<string, string> = {
  INVITATION_EXPIRED: 'This invitation link has expired.',
  INVITATION_ALREADY_USED: 'This invitation link has already been used.',
  INVITATION_ALREADY_PENDING: 'An active invitation for this email already exists.',
  USER_ALREADY_EXISTS: 'An account with this email already exists.',
  PERMISSION_DENIED: 'You do not have permission to perform this action.',
  EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN: 'This employee already has an active onboarding plan.',
  // ...
}
```

**Every new backend error code must have a corresponding entry here.** Without it, users see the generic "Something went wrong. Please try again." fallback.

### `getErrorMessage` — `src/utils/getErrorMessage.ts`

```ts
export function getErrorMessage(err: unknown): string {
  const data = (err as { response?: { data?: { error_code?: string; message?: string } } }).response?.data
  if (data?.error_code && ERROR_MESSAGES[data.error_code]) {
    return ERROR_MESSAGES[data.error_code]
  }
  if (data?.message) {
    return data.message   // fallback: show backend's human-readable message
  }
  return 'Something went wrong. Please try again.'
}
```

Resolution order:
1. `error_code` found in `ERROR_MESSAGES` → localized string
2. `error_code` not mapped → backend `message` field (raw, but better than generic)
3. No response data → generic fallback

### Rule

> Every hook or component that calls an API and catches errors must use `getErrorMessage(err)` — never hardcode an error string like `'Failed to create plan.'`.
