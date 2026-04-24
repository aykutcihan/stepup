# Sprint 2 — Refinement

## Sprint Goal
Auth flow is fully working. HR Admin can invite users, invited users can register via invitation link, all users can log in and log out securely, RBAC is enforced across all routes, and deactivated users lose access immediately.

## User Stories Reviewed

### US-001: Invite User with Role
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — SendGrid API key needed in Secret Manager
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST, DOC, DEVOPS
- Questions / blockers: None

### US-002: Register via Invitation
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-001
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: None

### US-003: User Login & Logout
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-002
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST, DOC
- Questions / blockers: None

### US-004: Token Refresh
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-003
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: None

### US-005: Enforce Role-Based Access Control
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-003
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST, DOC
- Questions / blockers: None

### US-006: Invitation Expiration
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-001
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: None

### US-007: Force Logout for Deactivated Users
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-003
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: None

## Out of Scope Decisions
- Password reset flow — not in MVP
- Social login (Google, GitHub) — not in MVP

## Open Questions
- None

## Notes
- US-001 must be completed before US-002, US-006
- US-003 must be completed before US-004, US-005, US-007
- ADR-003 (state management) and ADR-004 (HttpOnly cookies) to be written during this sprint
