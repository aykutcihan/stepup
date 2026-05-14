# Sprint 6 — Refinement

## Sprint Goal
Employee can view their onboarding plan and work through tasks. Managers can approve or return completed tasks with feedback. The full task state machine is enforced.

## User Stories Reviewed

### US-014a: Employee Task Workflow — State Machine (#182)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — US-013 (plan creation) must be done, already merged
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: None

### US-014b: Employee Task Workflow — File Upload & Comments (#183)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — US-014a must be completed first; GCP Cloud Storage bucket needed
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: GCS bucket and service account credentials to be set up before implementation

### US-015: Manager Task Review (#130)
- Acceptance criteria clear? Yes
- Dependencies identified? Yes — depends on US-014a (task must reach COMPLETED status)
- Subtasks defined? Yes — BE, BE TEST, FE, FE TEST
- Questions / blockers: Presigned URL generation for file downloads depends on US-014b GCS setup

## Split Decision
US-014 was originally a single story. Split into US-014a and US-014b during Sprint 6 refinement.

**Reason:** File upload requires GCP Cloud Storage infrastructure (bucket, service account, google-cloud-storage package) which adds significant scope. The state machine (014a) is independently deliverable and unblocks US-015.

**Result:**
- US-014a (3 pts) — state machine only, no file I/O
- US-014b (5 pts) — attachments + comments, depends on 014a

## Out of Scope Decisions
- Presigned URL generation for manager download — deferred to US-015
- Overdue task detection — deferred to US-017 (Automated Scheduler)

## Open Questions
- None

## Notes
- US-014a must be merged before US-015 work begins (APPROVED / RETURNED enum values needed)
- US-014b can be worked in parallel with US-015 once US-014a is done
