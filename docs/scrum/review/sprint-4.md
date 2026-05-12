# Sprint 4 — Review

## Sprint Goal
HR Admin can create, manage, and clone onboarding templates. Templates have ordered tasks with deadlines and required/optional flags. Only one template can be active per department at a time.

## Sprint Goal Achieved?
Yes

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-023 | Template Management | Done | BE + FE + tests |
| US-011 | Seed Data — Sprint 4 | Done | Templates and template tasks seeded |
| US-012 | ADR Documentation — Sprint 4 | Done | ADR-008, ADR-009 added |

## Incomplete User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|

## Metrics
- USs planned: 3
- USs completed: 3
- USs carried over: 0

## Notes
- `values_callable` pattern established for SQLAlchemy enum autogenerate (documented in enum conventions)
- `expire_on_commit=False` added to test session for relationship-heavy responses
- E2E Sprint 2 tests completed during this sprint
