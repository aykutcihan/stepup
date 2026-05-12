# Sprint 5 — Review

## Sprint Goal
HR Admin can create onboarding plans for employees from templates. Employees can view their plan and work through tasks. Managers can approve or return completed tasks with feedback. The full task state machine is enforced.

## Sprint Goal Achieved?
Partially

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-013 | Plan Creation & Administration | Done | BE + FE + tests — HR Admin flow complete |

## Incomplete User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-014 | Employee Task Workflow | Not started | Sprint 6 |
| US-015 | Manager Task Review | Not started | Sprint 6 |

## Metrics
- USs planned: 3
- USs completed: 1
- USs carried over: 2

## Notes
- US-013 covers HR Admin side: create plan, view detail, cancel tasks, adjust deadlines, change manager, add tasks
- Task status enum scoped to `not_started` / `cancelled` only (YAGNI) — remaining statuses added in US-014
- Plans sidebar nav added; plan list page deferred to US-018 dashboard sprint
