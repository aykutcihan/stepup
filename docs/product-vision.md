# StepUp — Product Vision

**Version:** 1.0  
**Date:** 2026-04-21  
**Owner:** Developer (Solo Project)  
**Status:** Living document — will evolve throughout development  

--- 

## Executive Summary

StepUp is a web-based employee onboarding management system designed to streamline the process of integrating new team members into an organization.

The system provides a structured workflow for assigning, tracking, completing, and approving onboarding tasks while maintaining clear audit trails, automated notifications, and real-time progress visibility for all parties involved.

**Target Users:** Organizations of any size that onboard new employees and want to replace email chains, spreadsheets, and ad-hoc processes with a transparent, auditable, and standardized system.

---

## Vision Statement

> "Enable organizations to onboard new employees efficiently — with clear task ownership, transparent progress tracking, and zero steps falling through the cracks."

---

## The Problem We're Solving

### Current State (Without StepUp)

Organizations typically manage onboarding through:

- **Email chains** — difficult to track, easy to lose, no audit trail
- **Spreadsheets** — manual updates, no automation, prone to human error
- **Ad-hoc processes** — inconsistent across departments, depends on who you ask
- **Verbal instructions** — nothing documented, knowledge lost when people leave

**Pain Points:**

- New employees don't know what they need to do or in what order
- Managers lose track of which tasks are pending or overdue
- HR has no visibility into onboarding progress across the organization
- No standardized process across departments
- Documents get lost or submitted to the wrong person
- Time wasted on follow-up emails and status checks
- No record of who approved what and when

### Future State (With StepUp)

- Self-service portal for employees to view and complete their onboarding tasks
- Automated task assignment from department-specific templates
- Real-time progress visibility for all parties
- Email notifications at each workflow stage
- Complete audit trail of all actions
- Standardized onboarding process across the organization
- Dashboard for managers and HR admins

---

## User Roles

### 1. Employee

**Who:** Any new employee joining the organization

**Capabilities:**
- View assigned onboarding plan and task list
- Mark tasks as completed
- Upload required documents per task
- Add comments or questions to tasks
- Track own onboarding progress
- Receive email notifications on task assignments and status changes

**Use Case Examples:**
- "I need to complete my employment contract and upload it"
- "I need to finish the company policy training"
- "I need to request access to the development environment"

---

### 2. Manager / Team Lead

**Who:** Direct managers, team leads, department heads

**Capabilities:**
- View onboarding plans of all direct reports
- Approve or return completed tasks with feedback
- Assign tasks manually outside of templates
- Set or adjust task deadlines
- View team-wide onboarding progress dashboard
- Add comments and feedback to tasks
- Receive email notifications for completed tasks awaiting approval

**Decision Criteria:**
- Task completed correctly and completely
- Required documents uploaded and valid
- Quality of work meets department standards

---

### 3. HR Admin

**Who:** HR administrators, people operations team

**Capabilities:**
- Create and manage onboarding templates per department
- Register new employees and assign onboarding plans
- View system-wide onboarding progress
- Manage user accounts and roles
- Generate reports and analytics
- Export data to CSV / PDF
- View full audit trail
- Manage system configuration

**Responsibilities:**
- Template management
- User management
- Compliance and audit
- Reporting and analytics

---

## Core Workflow

StepUp implements a three-step workflow:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    STEP 1:      │     │    STEP 2:      │     │    STEP 3:      │
│    Assign       │ ──► │    Complete     │ ──► │    Approve      │
│                 │     │                 │     │                 │
│ HR creates plan │     │ Employee works  │     │ Manager reviews │
│ from template.  │     │ on tasks and    │     │ and approves or │
│ Tasks auto-     │     │ marks them      │     │ returns tasks   │
│ assigned.       │     │ complete.       │     │ with feedback.  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Workflow States

### Task States

| State | Description | Who Can Act |
|---|---|---|
| **Not Started** | Task assigned, not yet worked on | Employee |
| **In Progress** | Employee has started the task | Employee |
| **Completed** | Marked done by employee | Manager |
| **Approved** | Verified and approved by manager | — (terminal) |
| **Returned** | Sent back with feedback | Employee |
| **Overdue** | Deadline passed, not completed | System (auto) |
| **Cancelled** | Task removed from plan | HR Admin |

### Onboarding Plan States

| State | Description |
|---|---|
| **Active** | Plan in progress |
| **Completed** | All tasks approved |
| **On Hold** | Paused by HR or Manager |
| **Cancelled** | Plan cancelled |

### State Transition Rules

- `Not Started` → `In Progress` — employee starts working
- `In Progress` → `Completed` — employee marks done
- `Completed` → `Approved` — manager approves
- `Completed` → `Returned` — manager returns with feedback
- `Returned` → `In Progress` — employee revises and resubmits
- Any non-terminal state → `Overdue` — system auto-marks when deadline passes
- `Overdue` → `In Progress` — employee can still complete after deadline

Invalid transitions return HTTP 400 with a descriptive error message.

---

## Key Features (MVP)

### For Employees

**1. Onboarding Dashboard**
- View all assigned tasks in one place
- Progress indicator (e.g. "8 of 12 tasks completed")
- Color-coded status: green = approved, amber = in progress, red = overdue
- Deadline visibility for each task

**2. Task Completion**
- Mark task as in progress or completed
- Upload documents per task (PDF, DOCX, PNG — max 10MB)
- Add comments or questions
- View manager feedback on returned tasks

**3. Notifications**
- Email on new task assignment
- Email on task approved or returned
- Email reminder 2 days before deadline

---

### For Managers

**1. Team Dashboard**
- Overview of all direct reports' onboarding progress
- Count of tasks awaiting approval
- Overdue task alerts

**2. Task Review**
- View full task details and uploaded documents
- Approve with optional comment
- Return with mandatory feedback
- View employee's task history

**3. Notifications**
- Email when employee completes a task awaiting approval
- Daily digest of pending approvals (optional)

---

### For HR Admins

**1. Template Management**
- Create onboarding templates per department
- Add tasks with title, description, deadline rules (e.g. "due 3 days after start")
- Set task order and dependencies (optional)
- Mark tasks as required or optional
- Clone and modify existing templates

**2. Onboarding Plan Management**
- Register new employee and generate plan from template
- Assign manager to employee
- Adjust plan after creation if needed

**3. User Management**
- Invite new users by email with role and department pre-assigned
- Edit, deactivate and reactivate user accounts
- Manage department structure

**4. Reporting & Analytics**
- Average onboarding completion time per department
- Task completion rates
- Bottleneck identification (which tasks take longest)
- Overdue task reports
- Export to CSV and PDF

**5. Audit Trail**
- Complete history of all actions in the system
- Who did what, when, on which entity
- Search and filter capabilities
- Cannot be modified or deleted

---

## Non-Functional Requirements

### Performance
- Page load time < 2 seconds
- API response time < 500ms for standard operations
- Support 100 concurrent users (initial target)
- Paginated list endpoints (default page size: 20)

### Security
- Role-based access control (RBAC) enforced on every endpoint
- JWT authentication with short-lived access tokens (15 min) and refresh tokens (7 days)
- Refresh tokens stored in database, revocable
- HttpOnly cookies — no tokens in localStorage
- HTTPS for all communications (GCP Cloud Run provides this automatically)
- Input validation and sanitization on all endpoints (Pydantic)
- SQL injection prevention via SQLAlchemy ORM
- XSS protection via Content Security Policy headers
- Rate limiting on authentication endpoints (5 requests/minute)
- CORS restricted to frontend domain only
- Secrets managed via GCP Secret Manager — no `.env` files in repository
- File upload validation: MIME type check, size limit (10MB), allowed types only
- OWASP ZAP security scan before final release

### Reliability
- 99% uptime during business hours
- Health check endpoint at `/health`
- Graceful error handling — no stack traces exposed to client
- Request ID on every request for traceability in logs
- Automated daily database backups (GCP Cloud SQL)

### Usability
- Mobile-responsive design (Tailwind CSS, mobile-first)
- Consistent UI patterns using shadcn/ui component library
- Loading states on all async operations
- Empty states with helpful guidance
- Error messages that are human-readable
- Confirmation dialogs for destructive actions
- Toast notifications for user actions

### Maintainability
- Clean architecture: Router → Service → Repository → Model
- Soft delete on all entities (`deleted_at` timestamp)
- Alembic migrations for all schema changes — no manual DB edits
- ADR documents for all major technical decisions
- Automated tests (unit, integration, E2E)
- CI/CD pipeline — tests run on every PR, merge blocked on failure
- Code linting enforced (Ruff for Python, ESLint for TypeScript)

---

## Technical Stack

| Layer | Technology | Reason |
|---|---|---|
| **Backend** | Python 3.11 + FastAPI | Async support, automatic Swagger, Pydantic validation |
| **ORM** | SQLAlchemy 2.0 (async) | Type-safe queries, async support |
| **Migrations** | Alembic | Industry standard for SQLAlchemy |
| **Database** | PostgreSQL 15 | Relational integrity, full-text search, proven reliability |
| **Auth** | python-jose + passlib (bcrypt) | JWT handling, secure password hashing |
| **Email** | SendGrid | Reliable delivery, free tier sufficient for MVP |
| **File Storage** | GCP Cloud Storage | Native GCP integration, scalable |
| **Scheduler** | APScheduler | Deadline checks, notification jobs |
| **Rate Limiting** | slowapi | FastAPI-native rate limiting |
| **Frontend** | React 18 + TypeScript | Type safety, component ecosystem |
| **Routing** | React Router v6 | Standard React routing |
| **Server State** | React Query (TanStack) | API cache, loading/error states |
| **Client State** | Zustand | Lightweight, sufficient for auth + UI state |
| **Forms** | React Hook Form + Zod | Type-safe form validation |
| **UI Components** | shadcn/ui + Tailwind CSS | Pre-built accessible components |
| **HTTP Client** | Axios | Interceptors for auth token handling |
| **Date Handling** | date-fns | Lightweight, tree-shakeable |
| **Monorepo** | Turborepo + pnpm | Fast builds, single repo management |
| **Containerization** | Docker + docker-compose | Consistent dev environment |
| **CI/CD** | GitHub Actions | Automated test + deploy pipeline |
| **Deployment** | GCP Cloud Run (BE) + Firebase Hosting (FE) | Scalable, pay-per-use |
| **Database Hosting** | GCP Cloud SQL | Managed PostgreSQL, automated backups |
| **Secrets** | GCP Secret Manager | Secure environment variable management |
| **Project Management** | GitHub Projects | Sprint board, issues, PR tracking |
| **Testing (BE)** | pytest + httpx | Unit and integration tests |
| **Testing (FE)** | Vitest + React Testing Library | Component and unit tests |
| **Testing (E2E)** | Playwright | End-to-end browser automation |
| **Linting (BE)** | Ruff | Fast Python linter |
| **Linting (FE)** | ESLint + Prettier | Code style consistency |

---

## Architecture

### Monorepo Structure

```
stepup/
├── apps/
│   ├── backend/                  # FastAPI application
│   │   ├── app/
│   │   │   ├── api/              # Routers (controllers)
│   │   │   │   ├── v1/                # API versioning — /api/v1/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── templates.py
│   │   │   │   │   ├── plans.py
│   │   │   │   │   └── tasks.py
│   │   │   │   └── router.py          # Mounts all v1 routes under /api/v1
│   │   │   ├── services/         # Business logic
│   │   │   │   ├── auth_service.py
│   │   │   │   ├── task_service.py
│   │   │   │   ├── notification_service.py
│   │   │   │   └── audit_service.py
│   │   │   ├── repositories/     # Database queries
│   │   │   ├── models/           # SQLAlchemy models
│   │   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── core/             # Config, database, dependencies
│   │   │   ├── errors/           # Error handling package
│   │   │   │   ├── __init__.py        # Exception classes
│   │   │   │   ├── messages.py        # Error code + message constants
│   │   │   │   └── handlers.py        # FastAPI exception handlers
│   │   │   ├── enums/            # Shared enum types
│   │   │   └── workers/          # APScheduler jobs
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── conftest.py
│   │   ├── alembic/              # Database migrations
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   └── frontend/                 # React application
│       ├── src/
│       │   ├── app/              # App.tsx, router setup
│       │   ├── lib/              # apiClient.ts (axios + interceptor)
│       │   ├── stores/           # authStore.ts (Zustand)
│       │   ├── components/       # Shared components (RequireRole, ForbiddenPage)
│       │   ├── constants/        # routes.ts, apiEndpoints.ts, errorMessages.ts, userRoles.ts
│       │   ├── types/            # api.ts (auto-generated from OpenAPI)
│       │   ├── utils/            # getErrorMessage.ts
│       │   └── features/
│       │       ├── auth/
│       │       │   ├── pages/    # LoginPage.tsx + LoginPage.test.tsx
│       │       │   ├── hooks/    # useLoginForm.ts
│       │       │   ├── schemas/  # loginSchema.ts
│       │       │   └── services/ # authService.ts
│       │       ├── invitation/
│       │       │   ├── pages/    # RegisterPage.tsx, InviteUserPage.tsx + tests
│       │       │   ├── hooks/    # useRegisterForm.ts, useInviteUserForm.ts
│       │       │   ├── schemas/  # registerSchema.ts, inviteSchema.ts
│       │       │   └── services/ # invitationService.ts
│       │       └── users/
│       │           ├── pages/    # HRDashboard.tsx + HRDashboard.test.tsx
│       │           └── services/ # userService.ts
│       ├── tests/
│       │   ├── setup.ts          # Shared test setup only (jest-dom import)
│       │   └── e2e/              # Playwright E2E tests
│       ├── Dockerfile
│       └── package.json
│
├── packages/
│   └── shared-types/             # Shared TypeScript types
│
├── docs/
│   ├── adr/                      # Architecture Decision Records
│   │   ├── ADR-001-fastapi.md
│   │   ├── ADR-002-gcp-stack.md
│   │   ├── ADR-003-state-management.md
│   │   ├── ADR-004-jwt-httonly-cookie.md
│   │   └── ADR-005-monorepo-turborepo.md
│   └── product-vision.md         # This document
│
├── .github/
│   └── workflows/
│       ├── ci.yml                # Run tests on every PR
│       └── deploy.yml            # Deploy to GCP on merge to main
│
├── docker-compose.yml            # Local development
├── turbo.json                    # Turborepo config
├── pnpm-workspace.yaml
└── README.md
```

### Error Handling Strategy

All error-related code lives in `app/errors/` — a dedicated package separate from `core/`. No scattered try/catch blocks across the codebase.

```
app/errors/
    __init__.py    ← exception classes (BaseAppError, NotFoundError, ValidationError, ...)
    messages.py    ← error code + message tuples (INVITATION_NOT_FOUND, ...)
    handlers.py    ← FastAPI exception handlers, registered in main.py
```

**Exception hierarchy:**
```python
BaseAppError
├── NotFoundError
├── ValidationError
├── AuthorizationError
└── ConflictError
```

Subclasses are added as needed — not pre-emptively.

**Consistent error response format across all endpoints:**
```json
{
  "success": false,
  "error_code": "INVITATION_NOT_FOUND",
  "message": "Invitation not found"
}
```

The `error_code` field allows the frontend to display localized messages without relying on backend message strings. Error messages are centralized in `app/errors/messages.py` — no magic strings in service or handler code.

### Frontend Constants Strategy

All magic strings and numbers on the frontend are centralized in `src/constants/`:

```typescript
// constants/routes.ts
export const ROUTES = {
  LOGIN: '/login',
  EMPLOYEE_DASHBOARD: '/employee/dashboard',
  MANAGER_DASHBOARD: '/manager/dashboard',
  HR_DASHBOARD: '/hr/dashboard',
  PLAN_DETAIL: (planId: string) => `/plans/${planId}`,
}

// constants/apiEndpoints.ts
export const API = {
  AUTH: {
    LOGIN: '/auth/login',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
  },
  TASKS: {
    COMPLETE: (taskId: string) => `/tasks/${taskId}/complete`,
    APPROVE: (taskId: string) => `/tasks/${taskId}/approve`,
  },
}

// constants/errorMessages.ts
export const ERROR_MESSAGES: Record<string, string> = {
  TASK_NOT_FOUND: 'This task no longer exists.',
  INVALID_STATE_TRANSITION: 'This action is not allowed at this stage.',
  FILE_TYPE_NOT_ALLOWED: 'Only PDF, DOCX, and PNG files are accepted.',
  OPTIMISTIC_LOCK_ERROR: 'Someone else updated this task. Please refresh.',
}
```

The `errorMessages.ts` file maps backend `error_code` values directly to user-facing strings. This makes i18n straightforward — swap the map for Dutch and the entire app speaks Dutch.

---

### Logging Strategy

All application logs are structured JSON and sent to **GCP Cloud Logging**. Every log line includes the `request_id` so a full request trace can be reconstructed from a single ID.

**Log levels:**
```
DEBUG   → local development only, never in production
INFO    → request received, task state changed, email sent
WARNING → unexpected but handled situation (e.g. overdue task detected)
ERROR   → unhandled exception, external service failure
```

**What is logged:**
```
✅ Every incoming request (method, path, status, duration, request_id)
✅ State machine transitions (task_id, old_state, new_state, user_id)
✅ Email send attempts and outcomes
✅ File upload events (file_name, size, user_id — no file content)
✅ Auth events (login, logout, token refresh — no passwords)
✅ Scheduler job runs (job name, tasks processed, errors)
```

**What is never logged:**
```
❌ Passwords or tokens
❌ Full file contents
❌ Personal data beyond user_id (no names, emails in log lines)
❌ Request/response body content (only metadata)
```

This approach keeps logs useful for debugging while avoiding PII exposure — important for GDPR compliance in the Netherlands.

---

```
┌─────────────────────────────────────────────┐
│                   GCP Project               │
│                                             │
│  Firebase Hosting        Cloud Run          │
│  ┌──────────────┐       ┌──────────────┐   │
│  │   Frontend   │ ────► │   Backend    │   │
│  │  (React SPA) │       │  (FastAPI)   │   │
│  └──────────────┘       └──────┬───────┘   │
│                                │           │
│              ┌─────────────────┼──────┐    │
│              │                 │      │    │
│    ┌─────────▼──┐    ┌────────▼───┐  │    │
│    │ Cloud SQL  │    │   Cloud    │  │    │
│    │ PostgreSQL │    │  Storage   │  │    │
│    └────────────┘    └────────────┘  │    │
│                                      │    │
│    ┌──────────────┐  ┌─────────────┐ │    │
│    │   Secret     │  │   Cloud     │ │    │
│    │   Manager    │  │    Build    │ │    │
│    └──────────────┘  └─────────────┘ │    │
└─────────────────────────────────────────────┘
```

### Database Schema (Key Tables)

```
users               → id, email, password_hash, role, department_id,
                      manager_id, is_active, deleted_at, created_at

departments         → id, name, deleted_at, created_at

onboarding_templates → id, name, department_id, created_by,
                       is_active, deleted_at, created_at

template_tasks      → id, template_id, title, description, order,
                      deadline_days, is_required, deleted_at

onboarding_plans    → id, user_id, template_id, manager_id,
                      start_date, is_active, deleted_at, created_at

onboarding_plan_tasks → id, plan_id, template_task_id, title,
                        description, status, deadline,
                        is_required, order, return_comment,
                        deleted_at, created_at

task_comments       → id, plan_task_id, user_id, content, created_at

task_attachments    → id, plan_task_id, user_id, file_name,
                      file_url, file_type, file_size, created_at

audit_logs          → id, user_id, action, entity_type, entity_id,
                      old_value, new_value, request_id, created_at

notifications       → id, user_id, type, content, is_read,
                      related_entity_type, related_entity_id, created_at
```

**Key indexes:**
```sql
idx_plan_tasks_assigned    ON plan_tasks(plan_id, status)
idx_plan_tasks_deadline    ON plan_tasks(deadline, status)
idx_audit_logs_entity      ON audit_logs(entity_type, entity_id)
idx_notifications_user     ON notifications(user_id, is_read)
idx_users_email            ON users(email)
```

---

## Security Approach

### Authentication Flow

```
1. User submits email + password
2. Backend verifies credentials (bcrypt)
3. Backend issues:
   - Access token (JWT, 15 min) → set as HttpOnly cookie
   - Refresh token (opaque, 7 days) → set as HttpOnly cookie, stored in DB
4. Client sends requests — browser attaches cookies automatically
5. On access token expiry → client calls /auth/refresh
6. On logout → refresh token deleted from DB, cookies cleared
```

### Authorization

Every endpoint checks:
1. Is the user authenticated? (valid JWT)
2. Does the user's role permit this action?
3. Does the user own this resource? (e.g. employee can only see own tasks)

### OWASP Coverage

| Risk | Mitigation |
|---|---|
| Broken Access Control | RBAC on every endpoint, resource ownership checks |
| Cryptographic Failures | bcrypt for passwords, HTTPS enforced, HttpOnly cookies |
| Injection | SQLAlchemy ORM, Pydantic input validation |
| Insecure Design | Threat modelling per feature, ADR documentation |
| Security Misconfiguration | GCP Secret Manager, CORS restricted, CSP headers |
| Vulnerable Components | Dependabot alerts, regular dependency updates |
| Auth Failures | Rate limiting on login, refresh token rotation |
| Data Integrity Failures | Optimistic locking on task updates (version column) |
| Logging Failures | Request ID on all logs, audit trail, no PII in logs |
| SSRF | File uploads validated by MIME type, no URL fetching |

---

## Testing Strategy

### Unit Tests (pytest / Vitest)
- All service layer functions
- State machine transition validation
- Deadline calculation logic
- Role permission checks
- Target: 70%+ coverage on service layer

### Integration Tests (pytest + httpx)
- All API endpoints
- Auth flow (login, refresh, logout)
- Role-based access (employee cannot access manager endpoints)
- File upload flow
- Email trigger verification (mocked SendGrid)

### E2E Tests (Playwright)
Key scenarios:
```
1. HR creates template → registers employee → plan auto-generated
2. Employee logs in → views tasks → completes task → uploads document
3. Manager logs in → sees pending approval → approves task
4. Manager returns task → employee receives notification → resubmits
5. System marks overdue task → employee and manager notified
```

### CI Integration
- All tests run on every PR via GitHub Actions
- PR cannot be merged if tests fail
- Coverage report posted as PR comment
- E2E tests run on staging environment after merge to main

---

## Documentation Plan

### README.md
```
- Project description + live demo link
- Screenshots / demo GIF
- Features list
- Tech stack table
- Local setup (docker-compose up)
- Environment variables reference
- How to run tests
- Architecture overview
- Contributing guide
```

### API Documentation
- Auto-generated Swagger at `/docs` (FastAPI)
- Every endpoint has summary, description, request/response examples
- Available publicly for demo purposes

### Architecture Decision Records (ADR)
```
ADR-001: FastAPI over Django/Flask
ADR-002: GCP stack selection
ADR-003: Zustand + React Query over Redux
ADR-004: HttpOnly cookies over localStorage
ADR-005: Monorepo with Turborepo
ADR-006: API versioning with /api/v1/ prefix
ADR-007: Structured logging to GCP Cloud Logging
```

---

## Product Roadmap

### Sprint 1 — Foundation ✅ Done
- Monorepo setup (Turborepo + pnpm)
- Docker + docker-compose local environment
- GCP project setup (Cloud Run, Cloud SQL, Secret Manager)
- GitHub Actions CI pipeline
- Database schema + Alembic migrations (User model)

### Sprint 2 — Authentication ✅ Done
- User invitation by email with role assignment
- Registration via invitation token link
- Login, logout, token refresh (HttpOnly cookies)
- Role-based access control (RBAC) on all endpoints
- Force logout on user deactivation

### Sprint 3 — User, Department & Profile Management ✅ Done
- Department CRUD + soft delete
- User management (list, assign to department, deactivate, reactivate)
- My Profile (view + update name)
- Seed data: users and departments

### Sprint 4 — Onboarding Template Management ✅ Done
- Template CRUD per department (create, edit, activate, deactivate)
- Task management within templates (add, edit, reorder, delete)
- Clone template
- Seed data: templates and template tasks
- ADR documentation sprint

### Sprint 5 — Onboarding Plan & Task Workflow ✅ Done
- ✅ HR Admin: create onboarding plan from template (auto-generate tasks with deadlines)
- ✅ HR Admin: cancel tasks, adjust deadlines, change manager, add tasks to active plan

### Sprint 6 — Task Workflow & Manager Review ✅ Done
- ✅ Employee: view onboarding plan, start/complete tasks (state machine enforced)
- ✅ Manager: pending approvals queue, approve or return tasks with mandatory feedback
- ✅ Department added to invitation — user auto-assigned on registration
- ✅ UI polish: user dropdown menu, template creation, clickable cards, role-specific profile routes
- ⬜ US-014b (file upload) deferred to Sprint 8

### Sprint 7 — Dashboards & Audit Trail ✅ Done
- ✅ Role-based dashboards: HR Admin (active users, plans, departments, pending approvals), Manager (active plans, pending approvals, team size), Employee (progress bar, task breakdown, next deadline)
- ✅ Audit trail: all key actions logged (user invited/registered/deactivated, plan created, task started/completed/approved/returned), HR Admin filter page
- ✅ Bug fixes: deactivated user login rejection, login form error display, return_comment persistence, playwright baseURL env var

### Sprint 8 — Notifications ✅ Done
- ✅ Email notifications via SendGrid — plan started (employee), task completed (manager), task approved/returned (employee)

### Sprint 9 — Scheduler, Reports, Seed & File Upload ✅ Done
- ✅ APScheduler wired into FastAPI lifespan — `mark_overdue_tasks` (00:05 UTC) and `send_deadline_reminders` (00:00 UTC) run daily
- ✅ `OVERDUE` task status added — tasks past deadline auto-marked; employee and manager emailed; overdue tasks remain actionable
- ✅ Admin reports — 3 endpoints (completion time by dept, task rates by template, bottlenecks) + CSV export + `ReportsPage` with date range filter
- ✅ Comprehensive seed data — 6 users, 3 templates, 10 template tasks, 3 plans with realistic task statuses, 17 audit log entries
- ✅ Fixed broken `audit_logs` migration chain
- ✅ File upload & comments (US-014b) — GCS bucket (`stepup-494114-attachments`, europe-west4), `TaskAttachment` + `TaskComment` models, signed URL download, MIME/size validation, expandable task panel in `EmployeePlanPage`

### Sprint 10 — Final Polish
- ✅ Critical bug fixes (US-021 — Technical quality & polish)
  - `return_comment` column was missing from DB — manager feedback silently lost on task return; model + migration added
  - `attachments` and `comments` missing from API responses — page reload lost uploaded files; Pydantic schema updated, `TaskAttachmentResponse` now serialises from ORM via `model_validator`
  - Manager review page could not see employee attachments — `ApprovalTaskResponse` extended
  - Employee could not see manager feedback — `return_comment` rendered in `EmployeePlanPage`
  - Overdue task showed both Start and Complete buttons simultaneously — FE button logic fixed
  - `PlanDetailPage` back link pointed to create-plan form; task status badge only showed two states
  - `handleApprove` had no error handling — silent failure removed task from list on API error
  - `OnboardingPlanTaskRepository.get_by_id` now eager-loads `attachments` and `comments` to prevent `MissingGreenlet` errors on async serialisation

### Bonus (If Time Allows)
- Multi-tenancy (organization_id on all tables)
- Dutch + English language support (i18n)
- Webhook system for external integrations
- Full-text search on tasks and templates (PostgreSQL tsvector)

---

## Out of Scope (Not in MVP)

- Multi-level approval chains (single approver per task only)
- Native mobile apps (responsive web only)
- Video or async communication features
- Integration with external HR systems (BambooHR, Workday, etc.)
- Slack / Teams notifications (webhook system planned for post-MVP)
- Recurring onboarding tasks
- Performance review features
- Payroll or contract management
- Single Sign-On (SSO / SAML)

---

## Success Metrics

### Usage
- Employee completes onboarding plan within expected timeframe
- Manager approval time < 24 hours per task
- Zero onboarding tasks lost or forgotten

### Technical
- API response time < 500ms (p95)
- Test coverage > 70% on service layer
- Zero critical security findings in OWASP ZAP scan
- CI pipeline passes on every merge to main

### Quality
- No critical bugs in production
- All endpoints documented in Swagger
- README enables a new developer to run the project locally in under 10 minutes

---

## Questions & Open Decisions

**Q: Can an employee edit a task after marking it complete?**  
A: No. Once marked complete, the employee can only wait for manager feedback. If returned, the task goes back to In Progress.

**Q: What happens if the manager account is deactivated?**  
A: HR Admin must reassign the manager before deactivation. The system blocks deactivation if pending approvals exist.

**Q: Can HR Admin approve tasks instead of the manager?**  
A: Yes, HR Admin has override capability. All overrides are recorded in the audit trail.

**Q: What happens to active plans if a template is deleted?**  
A: Templates use soft delete. Active plans are not affected. plan_tasks store a copy of the task title and description at time of plan creation.

**Q: Can a task have sub-tasks?**  
A: Not in MVP. Single-level tasks only. Sub-tasks may be considered post-MVP.

---

## Document History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-21 | Initial product vision document |
| 1.1 | 2026-04-21 | Added error handling strategy, frontend constants, logging strategy, API versioning, removed intern references |
| 1.2 | 2026-05-03 | Updated error handling to app/errors/ package, updated monorepo structure |
| 1.3 | 2026-05-12 | Sprints 2–4 marked done, Sprint 5 in progress; added reactivate to user management; updated onboarding_plans schema to match implementation |
| 1.4 | 2026-05-14 | Sprint 5 done, Sprint 6 done; task workflow and manager review complete; department added to invitation; US-014b deferred to Sprint 8; sprint numbering adjusted |
| 1.5 | 2026-05-14 | Sprint 7 done; role-based dashboards (US-018) and audit trail (US-019) complete; bug fixes (auth is_active, login error display, return_comment, playwright config); Sprint 8 scope updated |
| 1.6 | 2026-05-14 | US-016 email notifications done; plan started, task completed/approved/returned emails added via SendGrid |
| 1.7 | 2026-05-14 | Sprint 9 done; US-017 scheduler (OVERDUE status + APScheduler lifespan + 2 daily jobs), US-020 reports (3 endpoints + CSV + ReportsPage), comprehensive seed data, audit_log migration fix; Sprint 8 closed, Sprint 9 added, Sprint 10 scoped |
| 1.8 | 2026-05-14 | US-014b done; GCS bucket created, TaskAttachment + TaskComment models, signed URL downloads, EmployeePlanPage expandable panel; Sprint 9 updated, Sprint 10 reduced to US-021 only |
| 1.9 | 2026-05-15 | Sprint 10 US-021 done; critical bug fixes: return_comment DB column added, attachments/comments in API responses, manager review shows attachments, employee sees manager feedback, overdue button logic, PlanDetailPage navigation, error handling; DB schema updated |

**Review Frequency:** After each sprint  
**Status:** Living document — will evolve throughout the project
