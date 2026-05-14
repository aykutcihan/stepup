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

- ✅ US-016 Email Notifications
- ⬜ US-017 Automated Scheduler (deferred to Sprint 9)
- ⬜ US-020 Admin Reports (deferred to Sprint 9)
- ⬜ US-014b File Upload (deferred to Sprint 9)

## Sprint 9 — Scheduler, Reports & Quality
APScheduler marks overdue tasks daily and sends deadline reminders. HR Admin reports are live. Seed data covers all features. Quality polish and remaining US-021 work.

- ✅ US-017 Automated Scheduler (APScheduler lifespan, mark_overdue_tasks, send_deadline_reminders, OVERDUE enum)
- ✅ US-020 Admin Reports & Export (3 endpoints, CSV export, ReportsPage with date filter)
- ✅ Comprehensive seed data (alice, bob, manager2, Product template, 3 plans, 17 audit logs)
- ⬜ US-014b File Upload
- ⬜ US-021 Technical Quality & Polish

## Sprint 10 — Final Polish & File Upload
All list endpoints are paginated. File upload via GCS. Full E2E regression suite passes in CI. README and Swagger polished for demo.
