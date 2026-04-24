# Guide: User Story and Issue Management Strategy

This guide documents how user stories are written, structured, and pushed to GitHub for the StepUp project.

---

## User Story Format

Every US follows this structure:

```
As a [role],
I want to [action],
So that [benefit].
```

**Roles in StepUp:** HR Admin, Manager, Employee, System (for automated/background tasks)

Each US has:
- A clear title: `US-XXX: Short description`
- A parent epic
- A user story in the format above
- Acceptance criteria (specific, testable conditions)
- Sub-issues (see below)

---

## Epic Structure

USs are grouped into epics. Epics are also GitHub issues — they provide a high-level grouping for the project board.

| Epic | Sprint | US Range |
|------|--------|----------|
| Epic 1: Authentication, Authorization & User Management | Sprint 2 | US-001 – US-007 |
| Epic 2: User & Department Management | Sprint 3 | US-008 – US-011 |
| Epic 3: Onboarding Template Management | Sprint 4 | US-012 – US-014 |
| Epic 4: Onboarding Plan Management | Sprint 5 | US-015 – US-020 |
| Epic 5: Notifications & Email | Sprint 6 | US-021 – US-025 |
| Epic 6: Dashboards | Sprint 7 | US-026 – US-028 |
| Epic 7: Attachments | Sprint 8 | US-029 |
| Epic 8: Audit Trail | Sprint 9 | US-030 |
| Epic 9: Reporting & Analytics | Sprint 9 | US-031 |
| Epic 10: System & Quality | Sprint 10 | US-032 – US-034 |

---

## Subtask Structure

Every US is broken into subtask issues. Subtasks are separate GitHub issues linked to the parent US as sub-issues.

### Fixed subtasks — present in every US that has both BE and FE work:

| Subtask | When to open | What it covers |
|---------|-------------|----------------|
| BE | Always (if backend work exists) | Model, service, endpoint, seed update |
| BE TEST | Always (if BE subtask exists) | pytest unit + integration tests |
| FE | Always (if frontend work exists) | Component, API connection, route |
| FE TEST | Always (if FE subtask exists) | Vitest unit tests |

### Optional subtasks — only when the US requires it:

| Subtask | When to open | Example |
|---------|-------------|---------|
| DOC | New technical concept, new guide, or ADR decision | US-003: auth flow guide, US-005: RBAC ADR |
| DEVOPS | Infrastructure change, new GCP service, new secret, docker-compose change | US-001: SendGrid secret to Secret Manager, US-029: Cloud Storage bucket |
| E2E | Once per sprint — critical user journey only | Sprint 2: Login → Dashboard flow |

### Rule for DOC:
Open a DOC subtask when someone new to the codebase would need a written explanation to understand what was built and why. If it is just "I wrote an endpoint", no DOC needed. If it introduces a new pattern (state machine, soft delete, auth flow), DOC is needed.

### Rule for DEVOPS:
Open a DEVOPS subtask when any of the following change:
- A new GCP service is used (Cloud Storage, APScheduler on Cloud Run, etc.)
- A new secret is added to Secret Manager
- `docker-compose.yml` changes
- CI/CD pipeline changes
- A new environment variable is introduced

### Rule for E2E:
- One E2E issue per sprint, opened at the end of the sprint
- Covers only the most critical user journey introduced in that sprint
- Written with Playwright
- Must pass in CI pipeline

---

## Subtask Timing

**Do not open subtasks when the US is created.**

Open subtasks at the start of the sprint when that US will be worked on.

Example workflow:
1. Sprint 2 starts
2. Open subtask issues for all Sprint 2 USs using VS Code AI (see below)
3. Add `subtask` label to all subtask issues
4. Work on each subtask, close it when done
5. At the end of the sprint, open the E2E subtask issue
6. Close the E2E issue when the test passes in CI

---

## GitHub Issue Templates

All issues are created using templates stored in `.github/ISSUE_TEMPLATE/`.

| Template file | Used for |
|--------------|----------|
| `us.yml` | Main US issue |
| `subtask-be.yml` | BE subtask |
| `subtask-be-test.yml` | BE TEST subtask |
| `subtask-fe.yml` | FE subtask |
| `subtask-fe-test.yml` | FE TEST subtask |
| `subtask-devops.yml` | DEVOPS subtask (optional) |
| `subtask-e2e.yml` | E2E subtask (one per sprint) |
| `subtask-doc.yml` | DOC subtask (optional) |

Blank issues are disabled — every issue must use a template.

---

## How to Push Issues to GitHub

For bulk issue creation, use the VS Code AI assistant with a prompt that uses the full `gh.exe` path.

**Important:** `gh` CLI must be called with its full path in VS Code terminal on Windows:
```
C:\Program Files\GitHub CLI\gh.exe
```

Running `bash setup.sh` does not work because bash on Windows uses its own PATH and cannot find `gh`. Always use VS Code AI with PowerShell and the full `gh.exe` path.

**Prompt structure for VS Code AI:**
```
gh is installed at: C:\Program Files\GitHub CLI\gh.exe
Repository: aykutcihan/stepup

Run all commands using the full path "C:\Program Files\GitHub CLI\gh.exe".
Run in PowerShell terminal inside VS Code.
Do not ask for confirmation — execute all commands one by one.

[list of gh issue create commands]
```

For single issues, use the GitHub web interface — templates are available automatically when creating a new issue.

---

## How to Open Sprint Subtasks

At the start of each sprint, prepare a prompt for VS Code AI with all subtask issues for that sprint.

Each subtask issue must include:
- Title format: `BE: US-XXX Description` / `FE TEST: US-XXX Description` etc.
- Body: Parent US reference, Scope, Acceptance Criteria, Definition of Done
- Labels: sprint label + subtask type label (backend, frontend, testing, devops, documentation)

After all subtask issues are created:

**Add `subtask` label to all of them:**
```
Add the label "subtask" to issues #XX, #XX, #XX...
Use: & "C:\Program Files\GitHub CLI\gh.exe" issue edit NUMBER --repo aykutcihan/stepup --add-label "subtask"
```

**Note on sub-issues:** GitHub's sub-issue API is not available on the Free plan. As a workaround, each subtask issue references its parent US in the body. You can also link them manually from the issue sidebar on GitHub.

---

## GitHub Project Board Structure

The project board has three views:

| View | Filter | Purpose |
|------|--------|---------|
| `Backlog` | none | All issues across all sprints |
| `Sprint X — US` | `label:sprint-X -label:subtask` | Current sprint — US and Epic issues only (clean working view) |
| `Sprint X — Full` | `label:sprint-X` | Current sprint — US + all subtask issues |

**Working view:** Always use `Sprint X — US` during development. It shows only 9–12 items (Epics + USs + E2E) — no noise from subtasks.

**How to set a filter in GitHub Projects:**
1. Open the view
2. Click the filter bar at the top
3. Type the filter (e.g. `label:sprint-2 -label:subtask`)
4. Press Enter
5. Click Save

**When a new sprint starts:**
- Create two new views: `Sprint X — US` and `Sprint X — Full`
- Update filters with the new sprint label

---

## Seed Data Strategy

Seed data is not a standalone US. It is part of the BE subtask of each sprint.

Each sprint's BE subtask includes: "Update seed with data for tables introduced in this sprint."

| Sprint | Seed update |
|--------|-------------|
| Sprint 2 | Add users (HR Admin, Manager, Employee) |
| Sprint 3 | Add departments, assign users |
| Sprint 4 | Add templates and template tasks |
| Sprint 5 | Add plans and plan tasks in various states |
| Sprint 6 | Add notification log entries |
| Sprint 10 | US-032: finalize seed as realistic idempotent demo dataset |

Command to run seeder locally:
```bash
docker-compose run --rm backend python -m seeder
```

---

## Definition of Done for a US

A US is Done when all of the following are true:
- All subtask issues are closed
- All tests pass in CI pipeline
- PR is reviewed and merged to develop
- Acceptance criteria in the US issue are all checked off