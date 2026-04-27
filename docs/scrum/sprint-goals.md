# Sprint Goals

## Sprint 1 — Foundation
Set up the development foundation: monorepo, Docker, GCP infrastructure, CI pipeline, and database schema. The project should be ready for feature development by the end of this sprint.

## Sprint 2 — Authentication
Auth flow is fully working. HR Admin can invite users by email with a role. Invited users can register via a secure token link. All users can log in and log out. Sessions stay active via token refresh. RBAC is enforced on all routes. Deactivated users lose access immediately.

## Sprint 3 — User, Department & Profile Management
HR Admin can manage departments and users in one admin panel. Users can be assigned to departments. Every user can view and update their own profile. Seed data covers all users and departments.

## Sprint 4 — Onboarding Template Management
HR Admin can create onboarding templates with ordered tasks per department. Templates can be activated, deactivated, and cloned. Only one template can be active per department at a time. ADR-003 and ADR-004 are documented.

## Sprint 5 — Onboarding Plan & Task Workflow
HR Admin can create onboarding plans for employees from templates. Employees can view their plan, work through tasks, upload attachments, and add comments. Managers can approve or return tasks with feedback. HR Admin can adjust active plans.

## Sprint 6 — Notifications, Scheduler & Dashboards
Email notifications are sent at every key workflow stage via SendGrid. APScheduler automatically marks overdue tasks and sends deadline reminders daily. All three roles have a dedicated dashboard showing relevant data.

## Sprint 7 — Audit Trail, Reports & Quality
Every action in the system is logged in an uneditable audit trail. HR Admin can generate and export reports. All list endpoints are paginated. Health check endpoint is in place. Full E2E regression passes in CI. README and Swagger are polished.