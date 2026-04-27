# Sprint 2 — Refinement

## Sprint Goal
Auth flow is fully working. HR Admin can invite users by email with a role. Invited users can register via a secure token link. All users can log in and log out. Sessions stay active via token refresh. RBAC is enforced on all routes. Deactivated users lose access immediately.

## User Stories Reviewed

### US-001: User Invitation & Registration (5 points)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — SendGrid API key needed in Secret Manager before this ships
- Story covers: invite endpoint, registration endpoint, invitation expiration, resend
- Questions / blockers: None

### US-002: Login, Logout & Token Refresh (5 points)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-001 (user must exist to log in)
- Story covers: login, logout, refresh token rotation, HttpOnly cookies, rate limiting
- Questions / blockers: None

### US-003: Access Control & Security (3 points)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-002 (login must work before RBAC can be tested)
- Story covers: RBAC on all endpoints, role-based frontend routing, force logout on deactivation
- Questions / blockers: None

### E2E — Sprint 2 (not pointed — quality gate)
- Covers: login flow per role, role-based routing, deactivation, expired invitation
- Opens at end of sprint after all US stories are Done

## Out of Scope Decisions
- Password reset flow — not in MVP
- Social login (Google, GitHub) — not in MVP
- Two-factor authentication — not in MVP

## Open Questions
- None

## Notes
- US-001 must be completed before US-002 and US-003
- ADR-004 (HttpOnly cookies) will be written as part of US-002 DOC subtask
- ADR-003 (Zustand + React Query) moved to Sprint 4 — frontend state management decisions not needed until Sprint 4