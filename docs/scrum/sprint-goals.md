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

## Sprint 6 — Task Workflow & Manager Review
Employee can view their onboarding plan and work through tasks. Managers can approve or return completed tasks with mandatory feedback. The full task state machine is enforced.

## Sprint 7 — Dashboards & Audit Trail ✅ Done
All three roles have a dedicated dashboard with real system stats. Every key action is logged in an uneditable audit trail visible and filterable by HR Admins.

## Sprint 8 — Notifications, Scheduler, Reports & Attachments
Email notifications are sent at every key workflow stage. APScheduler automatically marks overdue tasks daily and sends deadline reminders. HR Admins have access to basic onboarding reports. Employees can upload documents to tasks stored in GCP Cloud Storage.

## Sprint 9 — Quality & Polish
All list endpoints are paginated. Seed data creates a realistic demo dataset. Full E2E regression suite passes in CI pipeline. README and Swagger polished for demo.
