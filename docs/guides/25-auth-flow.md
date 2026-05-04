# Auth Flow

## Overview

Authentication is cookie-based. Tokens are stored in HttpOnly cookies — JavaScript cannot access them.

## Token Types

| Token | Storage | Expiry | Purpose |
|-------|---------|--------|---------|
| `access_token` | HttpOnly cookie | 15 minutes | Authenticate each request |
| `refresh_token` | HttpOnly cookie + DB | 7 days | Issue new access tokens |

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

The `Limiter` instance is created once in `main.py` and registered on `app.state.limiter`. Endpoints import it from `main.py` — this ensures a single shared counter across the application. Creating a separate `Limiter` in each router would result in isolated counters that bypass the global limit.

## Key Files

| File | Responsibility |
|------|---------------|
| `app/core/security.py` | Token creation and decoding |
| `app/core/dependencies.py` | `get_current_user` dependency |
| `app/core/constants.py` | Cookie name constants |
| `app/services/auth_service.py` | Login, logout, refresh logic |
| `app/repositories/refresh_token_repository.py` | Refresh token DB operations |
