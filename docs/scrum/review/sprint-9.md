# Sprint 9 — Review

## Sprint Goal
APScheduler marks overdue tasks daily and sends deadline reminders. HR Admin reports are live. Seed data covers all features end-to-end.

## Sprint Goal Achieved?
Yes — US-017, US-020, and seed data fully delivered.

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-017 | Automated Scheduler | Done | APScheduler lifespan, 2 daily jobs, OVERDUE enum + migration, 3 email templates, 9 unit tests |
| US-020 | Admin Reports & Export | Done | 3 report endpoints, CSV export per endpoint, ReportsPage with date range filter, 10 BE + 5 FE tests |
| Seed | Comprehensive seed data | Done | 6 users, 3 templates, 3 plans with varied statuses, 17 audit logs, migration chain fixed |

## Incomplete / Deferred User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-014b | File Upload & Comments | GCS infrastructure required | Sprint 10 |
| US-021 | Technical Quality & Polish | Natural last sprint | Sprint 10 |

## Metrics
- USs planned: 2 (US-017, US-020)
- USs completed: 2
- PRs merged: 2 (#192 Reports, #193 Scheduler)

## Key Decisions Made This Sprint

### APScheduler wired into FastAPI lifespan (not a separate process)
APScheduler runs inside the FastAPI process via `lifespan`. This is the simplest approach for Cloud Run (single process, no worker dyno). If job load grows, the scheduler can be extracted to a dedicated Cloud Run job triggered by Cloud Scheduler.

### OVERDUE tasks remain actionable via two transitions
`VALID_TRANSITIONS` updated to `dict[status, set[status]]`. OVERDUE → IN_PROGRESS (start) and OVERDUE → COMPLETED (complete directly). This handles both cases: task was NOT_STARTED when marked overdue, and task was IN_PROGRESS when marked overdue.

### Reports use direct SQL aggregations — no dedicated analytics layer
All three report queries run direct SQLAlchemy aggregations against `onboarding_plan_tasks` and `onboarding_plans`. No materialized views or separate analytics tables. Acceptable for current scale; can be optimized if report query time exceeds 1s in production.

### CSV export via `?format=csv` query param — no separate endpoint
Each report endpoint returns JSON by default and CSV when `?format=csv`. The FE uses `apiClient` with `responseType: blob` + `URL.createObjectURL` for download — avoids CORS issues since cookies are sent automatically.

### Seed is fully idempotent — skip if exists by fixed ID
All seed entities use fixed UUIDs. Each section checks for existence before inserting. Running the seed twice is safe. New entities are added by extending the constants, not by modifying logic.

### audit_logs migration chain was broken — fixed
`c9a4b2e1f8d3` referenced a lost parent `a3f1c8e2d047`. Fixed by repointing to `14e90742db5f` (the actual head). An inline `index=True` on the `action` column conflicted with the explicit `op.create_index` call — fixed by removing `index=True` from the column definition.

## Emails Added This Sprint

| Method | To | When |
|--------|----|------|
| `send_task_overdue_email` | Employee | Task deadline passed, marked OVERDUE |
| `send_task_overdue_manager_email` | Manager | Employee's task marked OVERDUE |
| `send_deadline_reminder_email` | Employee | Task deadline is in exactly 2 days |

## Notes
- `mark_overdue_tasks` runs at 00:05 UTC daily (after reminders) to avoid race conditions
- Scheduler jobs log summary: `tasks_marked=N, emails_sent=N, errors=N`
- Email failures inside jobs are caught per-task and logged — one failure does not abort the entire job run
- OVERDUE status displayed as red badge in `EmployeePlanPage`; Start and Complete buttons both visible on OVERDUE tasks
