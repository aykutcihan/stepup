# Auth Flow

## Overview

Authentication is cookie-based. Tokens are stored in HttpOnly cookies — JavaScript cannot access them.

## Three Token Types

This project uses three distinct tokens — do not confuse them:

| Token | Where stored | Expiry | Purpose |
|-------|-------------|--------|---------|
| `invitation_token` | DB — `invitations.token` | 7 days | One-time registration link |
| `access_token` | HttpOnly cookie | 15 minutes | Authenticate each request |
| `refresh_token` | HttpOnly cookie + DB | 7 days | Issue new access tokens |

### Invitation Token

Generated when HR Admin invites a user (`secrets.token_urlsafe(32)`). Sent via email as a link. When the user registers, the token is validated and marked as used (`used_at`). It can only be used once — expired or used tokens return a clear error.

Real-world analogy: a one-time activation code sent by SMS when opening a bank account.

### Access Token (JWT)

Generated on login. Stored as HttpOnly cookie — JavaScript cannot read it, browser sends it automatically with every request. `get_current_user` dependency reads and validates it on each protected endpoint.

Real-world analogy: a building access card that expires after 15 minutes.

### Refresh Token

Generated on login alongside the access token. Stored in both the browser (HttpOnly cookie) and the DB (`refresh_tokens` table). When the access token expires, the client calls `POST /auth/refresh` — the old refresh token is deleted and a new pair is issued (rotation). If the refresh token is also expired, the user must log in again.

Real-world analogy: a card renewal document that lets you get a new access card without going to the front desk.

## Login Flow

1. Client sends `POST /api/v1/auth/login` with `{email, password}`
2. Server verifies credentials
3. Server issues access token and refresh token
4. Both tokens are set as HttpOnly cookies in the response
5. Client receives `{"message": "Login successful"}` — no tokens in body

## Request Authentication

1. Browser automatically sends cookies with each request
2. `get_current_user` dependency reads `access_token` cookie
3. Token is decoded and validated
4. If valid, the `User` object is injected into the endpoint

## Token Refresh Flow

1. Client sends `POST /api/v1/auth/refresh` (browser sends cookies automatically)
2. Server reads `refresh_token` cookie
3. Server validates token against DB
4. Old refresh token is deleted (rotation)
5. New access token and refresh token are issued as cookies

## Logout Flow

1. Client sends `POST /api/v1/auth/logout`
2. Server deletes all refresh tokens for the user from DB
3. Server clears both cookies
4. Client is effectively logged out

## Cookie Names

Cookie names are defined in `app/core/constants.py`:

```python
ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"
```

## Rate Limiting

Login endpoint is rate limited to 5 requests per minute per IP via `slowapi`.

The `Limiter` instance is created once in `app/core/limiter.py` and registered on `app.state.limiter` in `main.py`. Endpoints import it from `core/limiter.py` — this ensures a single shared counter across the application.

**Why not import from `main.py` directly?** Importing `limiter` from `main.py` inside a router causes a circular import — `main.py` loads the router, the router loads `auth.py`, `auth.py` tries to import from `main.py` which is not yet fully initialized. Moving `limiter` to `core/limiter.py` breaks the cycle.

## get_current_user vs require_role

`get_current_user` answers: **who is making this request?**
- Reads `access_token` cookie
- Decodes JWT → gets `user_id`
- Fetches user from DB
- Checks `is_active`
- Returns the `User` object

`require_role` answers: **is this user allowed to do this?**
- Internally calls `get_current_user`
- Checks `user.role` against the allowed roles
- Raises 403 if not allowed

Usage:
```python
# Any authenticated user
current_user: User = Depends(get_current_user)

# HR Admin only
current_user: User = Depends(require_role(UserRole.HR_ADMIN))
```

`require_role` is a factory function — it takes roles as arguments and returns a dependency function. This is a standard FastAPI pattern for parameterized dependencies.

## Key Files

| File | Responsibility |
|------|---------------|
| `app/core/security.py` | Token creation and decoding |
| `app/core/dependencies.py` | `get_current_user` dependency |
| `app/core/constants.py` | Cookie name constants |
| `app/services/auth_service.py` | Login, logout, refresh logic |
| `app/repositories/refresh_token_repository.py` | Refresh token DB operations |
