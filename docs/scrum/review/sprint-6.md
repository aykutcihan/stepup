# Sprint 6 — Review

## Sprint Goal
Employee can view their onboarding plan and work through tasks. Managers can approve or return completed tasks with feedback. The full task state machine is enforced.

## Sprint Goal Achieved?
Yes

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-014a | Employee Task Workflow — State Machine | Done | BE + FE + tests |
| US-015 | Manager Task Review | Done | BE + FE + tests |

## Incomplete / Deferred User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-014b | Employee Task Workflow — File Upload & Comments | GCS infra required | Sprint 8 |

## Metrics
- USs planned: 3 (US-014, US-015 carried over from Sprint 5)
- USs completed: 2 (014a + 015)
- USs carried over: 1 (014b → Sprint 8)

## Key Decisions Made This Sprint

### US-014 split into 014a and 014b
US-014 was split during sprint refinement. File upload requires GCP Cloud Storage infra (bucket, service account, google-cloud-storage package) which is significant scope. State machine (014a) delivers independently and unblocks US-015.

### Department added to invitation flow
HR Admin can now select department when sending an invitation. On registration, the user is automatically assigned to that department. Eliminates the manual post-registration assignment step.

**BE changes:** `department_id` added to `Invitation` model, schema, service, endpoint, and migration.
**FE changes:** Department dropdown added to invitation form; `useInviteUserForm` loads active departments on mount.

### Pending invitations filter
`InvitationRepository.get_all()` previously returned all invitations including used and expired ones. Fixed to return only pending invitations (`used_at IS NULL AND expires_at > now()`).

### Enum migration must be manual
Alembic `--autogenerate` does not detect PostgreSQL enum value additions. Adding new values to an existing enum requires a manual `ALTER TYPE ... ADD VALUE` migration. Documented in migration `773982f996b3`.

### Role-specific profile routes
`/profile` was shared across all three role blocks in App.tsx. React Router v6 always matched the first block (HR Admin), causing 403 for managers and employees. Fixed with role-specific paths: `/manager/profile` and `/employee/profile`.

## UI Polish (Outside US Scope)

- **Invite User button** added to UsersPage header (was only accessible via sidebar link)
- **InviteUserPage** fully restyled — email, role, department fields with proper layout
- **DepartmentsPage** aligned with UsersPage — "+ Add Department" toggle button in header
- **TemplatesPage** — "+ New Template" button with inline form; create navigates to detail page
- **Template card** fully clickable (entire card navigates to detail); "View" button removed
- **Template Rename** added to kebab menu with inline edit (same pattern as Departments)
- **Departments kebab** label changed from "Edit name" to "Rename" for consistency
- **User dropdown menu** (hamburger ≡) added to all layouts (HR, Manager, Employee) — shows name, email, My Profile link, Logout
- **Role badge** removed from nav bar — role already visible in dropdown

## Notes
- All BE tests: 141 passing
- All FE tests: 61 passing
- Migration `773982f996b3`: adds IN_PROGRESS, COMPLETED, APPROVED, RETURNED to task status enum
- Migration `14e90742db5f`: adds department_id to invitations table
