# Sprint 7 — Review

## Sprint Goal
All three roles have a dedicated dashboard with real stats. Every key action in the system is logged in an audit trail. HR Admin can view and filter the full audit history.

## Sprint Goal Achieved?
Yes — dashboards and audit trail delivered. Reports (US-020) and remaining open issues deferred.

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-018 | Role-Based Dashboards | Done | BE stats endpoints + FE stat cards for all 3 roles |
| US-019 | Audit Trail | Done | Model, migration, repo, service, API endpoint, FE page |

## Incomplete / Deferred User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-020 | Admin Reports & Export | Not started — no blocking dependency, next sprint | Sprint 8 |
| US-016 | Email Notifications | Requires hooking into task/plan events across services | Sprint 8 |
| US-017 | Automated Scheduler | Depends on US-016 (deadline reminder emails) | Sprint 8 |

## Metrics
- USs planned: 3 (US-018, US-019, US-020)
- USs completed: 2
- USs deferred: 1 (US-020 → Sprint 8)

## Bug Fixes (Outside US Scope)

Four bugs identified through code review and fixed before US work:

| File | Bug | Fix |
|------|-----|-----|
| `auth_service.py` | Deactivated users could log in — token issued, then 401 on next request | Added `is_active` check in `login()` before issuing tokens |
| `useLoginForm.ts` | API errors silently logged to console — user saw no feedback on wrong password | Added `submitError` state; catch block sets it instead of `console.error` |
| `task_workflow_service.py` + `OnboardingPlanTask` | Manager's return comment validated but never persisted — no column on model | Added `return_comment: Text` column, Alembic migration, assignment in service |
| `playwright.config.ts` | `baseURL` hardcoded to Docker hostname — local test runs always failed | Reads `process.env.BASE_URL` with `http://localhost:5173` fallback |

## Key Decisions Made This Sprint

### Dashboard stats via dedicated `/dashboard` endpoints
Stats for each role are served from role-gated endpoints (`/api/v1/dashboard/hr`, `/manager`, `/employee`). Count methods added to existing repositories (`count_active()` on User, OnboardingPlan, Department; `count_completed_across_active_plans()` and `count_completed_by_manager()` on OnboardingPlanTask). Service layer orchestrates repo calls, no direct SQL in service.

### Audit log in separate post-commit transaction
`AuditService.log()` is called **after** the main `db.commit()` in every service method. This ensures:
- A bug in audit logging never rolls back the main operation
- Audit entry is only written for actions that actually committed

Each hook follows the pattern:
```python
# main operation
task.status = APPROVED
await db.commit()
await db.refresh(task)
# audit — separate commit
await audit_service.log(db, ...)
await db.commit()
```

### `AuditLog` model is append-only — no `TimestampMixin`
`AuditLog` does not extend `TimestampMixin` (which adds `updated_at` and `deleted_at`). Audit logs must never be updated or soft-deleted. Only `created_at` is stored. Indexes on `action` and `created_at` for filter/sort performance.

### Actions logged

| Action | Triggered by |
|--------|-------------|
| `user.invited` | HR Admin sends invitation |
| `user.registered` | New user completes registration |
| `user.deactivated` | HR Admin deactivates user |
| `user.reactivated` | HR Admin reactivates user |
| `user.updated` | HR Admin changes user role or department |
| `plan.created` | HR Admin creates onboarding plan |
| `plan.task_cancelled` | HR Admin cancels task within plan |
| `task.started` | Employee starts task |
| `task.completed` | Employee marks task complete |
| `task.approved` | Manager approves task |
| `task.returned` | Manager returns task with comment |

## Notes
- All previous BE tests still passing (141)
- All previous FE tests still passing (61)
- Migration `a3f1c8e2d047`: adds `return_comment` to `onboarding_plan_tasks`
- Migration `c9a4b2e1f8d3`: creates `audit_logs` table with two indexes
- Open US issues with completed code: #119, #120, #121, #123, #124, #125, #130, #182 — code done, GitHub issues not yet closed
