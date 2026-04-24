# Sprint Goals

## Sprint 1 — Foundation
Set up the development foundation: monorepo, Docker, GCP infrastructure, CI pipeline, and database schema. The project should be ready for feature development by the end of this sprint.

## Sprint 2 — Auth
Auth flow is fully working. HR Admin can invite users, invited users can register via invitation link, all users can log in and log out securely, RBAC is enforced across all routes, and deactivated users lose access immediately.

## Sprint 3 — User & Department
HR Admin can manage departments and users. Users can be assigned to departments. Every user can view and update their own profile.

## Sprint 4 — Template Management
HR Admin can create, manage, and clone onboarding templates. Templates have ordered tasks with deadlines and required/optional flags. Only one template can be active per department at a time.

## Sprint 5 — Plan & Task Workflow
HR Admin can create onboarding plans for employees from templates. Employees can view their plan and work through tasks. Managers can approve or return completed tasks with feedback. The full task state machine is enforced.

## Sprint 6 — Notifications & Scheduler
Email notifications are sent at every key workflow stage. APScheduler automatically marks overdue tasks daily and sends deadline reminders 2 days in advance.

## Sprint 7 — Dashboards
All three roles have a dedicated dashboard. Employees see their progress, managers see their team's status and pending approvals, HR Admins see system-wide onboarding health.

## Sprint 8 — Attachments
Employees can upload documents to tasks. Files are stored in GCP Cloud Storage, validated by MIME type, and accessible to managers via presigned URLs.

## Sprint 9 — Audit Trail & Reports
Every action in the system is logged in the audit trail. HR Admins can filter and export audit data. Basic onboarding reports are available with CSV export.

## Sprint 10 — Quality & Polish
All list endpoints are paginated. Seed data creates a realistic demo dataset. Health check endpoint is in place. Full E2E regression passes in CI pipeline.