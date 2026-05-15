# Sprint 8 — Review

## Sprint Goal
Email notifications are sent at every key workflow stage. APScheduler automatically marks overdue tasks daily and sends deadline reminders. HR Admins have access to basic onboarding reports. Employees can upload documents to tasks stored in GCP Cloud Storage.

## Sprint Goal Achieved?
Partially — US-016 (email notifications) delivered. US-017, US-020, US-014b deferred.

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-016 | Email Notifications | Done | 4 email types via SendGrid; hooks in plan and task workflow services |

## Incomplete / Deferred User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-017 | Automated Scheduler | Depends on deadline reminder email (US-016 prerequisite now done) | Sprint 9 |
| US-020 | Admin Reports & Export | No blocking dependency | Sprint 9 |
| US-014b | File Upload & Comments | GCS infrastructure required | Sprint 9 |

## Metrics
- USs planned: 4
- USs completed: 1
- USs deferred: 3

## Key Decisions Made This Sprint

### Email calls are fire-and-forget after commit
All email sends happen after `db.commit()` inside a `try/except` block. SendGrid failure is logged via `logger.error` but never raises — the main operation always succeeds regardless of email outcome. This matches the pattern established for audit logging.

### Recipient fetched via user_repository, not relationship
`task_workflow_service` already had the task and plan in scope. Rather than adding `selectinload` for employee/manager to plan queries (which would affect all callers), recipient users are fetched with a separate `user_repository.get_by_id()` call inside the email block. This keeps the change minimal and non-invasive.

### Emails sent

| Method | To | When |
|--------|----|------|
| `send_plan_started_email` | Employee | HR Admin creates onboarding plan |
| `send_task_completed_email` | Manager | Employee marks task complete |
| `send_task_approved_email` | Employee | Manager approves task |
| `send_task_returned_email` | Employee | Manager returns task — feedback comment included in email body |

## Notes
- No schema changes — email notifications are stateless (no DB writes)
- No migration needed
- US-017 (deadline reminder) is now unblocked — `send_deadline_reminder_email` method can be added to `EmailService` and called from the scheduler
