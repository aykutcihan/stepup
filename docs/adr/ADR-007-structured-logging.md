# ADR-007: Structured Logging to GCP Cloud Logging

**Date:** 2026-04-21
**Status:** Accepted

---

## Context

StepUp runs on GCP Cloud Run. When issues occur in production, logs need to be searchable, filterable, and traceable across a full request lifecycle. Plain text logs are difficult to query and do not integrate well with GCP's logging infrastructure.

Additionally, the application handles personal data (employee names, email addresses) and operates under GDPR in the Netherlands. Logging strategy must ensure no PII leaks into application logs.

---

## Decision

All application logs are structured JSON and sent to **GCP Cloud Logging**.

Every log line includes a `request_id` field so the full lifecycle of any request can be reconstructed from a single ID.

**Log levels:**
- `DEBUG` — local development only, never in production
- `INFO` — request received, task state changed, email sent
- `WARNING` — unexpected but handled situation (e.g. overdue task detected)
- `ERROR` — unhandled exception, external service failure

**What is logged:**
- Every incoming request: method, path, status code, duration, request_id
- Task state transitions: task_id, old_state, new_state, user_id
- Email send attempts and outcomes
- File upload events: file_name, size, user_id — no file content
- Auth events: login, logout, token refresh — no passwords or tokens

**What is never logged:**
- Passwords or tokens
- Full file contents
- Personal data beyond user_id (no names or email addresses in log lines)
- Request or response body content

---

## Alternatives Considered

**Plain text logs to stdout**
Cloud Run captures stdout by default. Plain text is simple but not queryable. Filtering by request_id or user_id requires grep — not practical in production. Ruled out.

**Sentry**
Sentry is excellent for error tracking and has a generous free tier. It could complement structured logging for error alerting. However, for Sprint 1 scope, GCP Cloud Logging covers the logging requirement without adding another external service dependency. Sentry can be added post-MVP.

**Datadog / New Relic**
Powerful observability platforms but overkill for a solo portfolio project. Both have costs that are not justified at this scale.

---

## Consequences

**Gained:**
- GCP Cloud Logging is native to the infrastructure — no extra service or SDK needed beyond `google-cloud-logging`
- Log Explorer in GCP Console allows filtering by `request_id`, `level`, `user_id` without any extra tooling
- Structured logs are queryable with Log-based metrics and alerts
- Privacy-aware logging approach reduces GDPR risk — no PII in log lines means no data subject requests for log data

**Trade-offs:**
- Structured JSON logging requires slightly more setup than `print()` or basic `logging.basicConfig()`
- Local development logs are JSON — less readable than plain text. A local formatter can be added to pretty-print in development.
- Developers must be disciplined about not logging PII — this is a convention, not enforced by tooling