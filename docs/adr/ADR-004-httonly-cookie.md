# ADR-004: HttpOnly Cookies for Token Storage

## Status
Accepted

## Context
Authentication tokens need to be stored on the client side. Two common approaches exist:

- **Bearer token in localStorage/memory**: Simple, works well for mobile and external APIs. If stored in localStorage, vulnerable to XSS attacks. If stored in memory, lost on page refresh.
- **HttpOnly cookie**: Browser stores the token automatically. JavaScript cannot access it, eliminating XSS risk. Requires server-side logout.

StepUp is a web application handling sensitive HR data. Security is a priority.

## Decision
Use **HttpOnly cookies** for both access and refresh tokens.

- `access_token` cookie — short-lived (15 minutes), HttpOnly, SameSite=Strict
- `refresh_token` cookie — long-lived (7 days), HttpOnly, SameSite=Strict, stored in DB

Tokens are never exposed in response bodies.

## Consequences
- JavaScript cannot read tokens — XSS attacks cannot steal credentials
- CSRF risk is mitigated by `SameSite=Strict`
- Logout must be server-side — the server clears cookies and deletes the refresh token from DB
- Swagger testing requires manual cookie injection — acceptable tradeoff for development
