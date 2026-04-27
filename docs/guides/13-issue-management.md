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
- A title: `US-XXX: Short description`
- A story point estimate
- A parent epic
- A user story in the format above
- Acceptance criteria (specific, testable conditions)
- Sub-issues as checkboxes (see below)

---

## Story Points

Fibonacci scale: 1, 2, 3, 5, 8, 13

Solo developer, 2-week sprint. Target capacity: 13-15 points per sprint.

| Points | Meaning |
|--------|---------|
| 1-2 | Small — half a day to 1 day |
| 3 | Medium — 1-2 days |
| 5 | Large — 3-4 days |
| 8 | Very large — nearly a full sprint |
| 13 | Too large — must be split |

Story points are written in the issue body under `## Story Points`.

---

## US Sizing Rule

**One US = one meaningful feature**, not one endpoint.

Examples of correct sizing:
- ✅ US-001: User Invitation & Registration (covers invite + register + expiration + resend)
- ✅ US-014: Employee Task Workflow (covers view plan + start/complete task + upload attachment)
- ❌ Too small: "Create invitation endpoint" as a US
- ❌ Too small: "Validate invitation token" as a separate US

If a US exceeds 8 points, split it. If two US cover the same screen or same user action, merge them.

---

## Epic Structure

USs are grouped into epics. Epics are GitHub issues with the `epic` label.

| Epic | Sprint | US Numbers |
|------|--------|------------|
| Epic 1: Authentication | Sprint 2 | US-001, US-002, US-003 |
| Epic 2: User & Department Management | Sprint 3 | US-004, US-005, US-022 |
| Epic 3: Template Management | Sprint 4 | US-023, US-011, US-012 |
| Epic 4: Plan & Task Workflow | Sprint 5 | US-013, US-014, US-015 |
| Epic 5: Notifications, Scheduler & Dashboards | Sprint 6 | US-016, US-017, US-018 |
| Epic 6: Audit, Reports & Quality | Sprint 7 | US-019, US-020, US-021 |

---

## Subtask Structure — Checkboxes Inside US Issue

Subtasks are **not separate issues**. They are checkboxes inside the US issue body under `## Sub-issues`.

### Fixed sections — present in every US that has BE and FE work:

```markdown
## Sub-issues

### BE
- [ ] Model: ...
- [ ] Migration: ...
- [ ] Service: ...
- [ ] Endpoint: ...
- [ ] Seed update

### BE TEST
- [ ] Unit test: ...
- [ ] Integration test: ...

### FE
- [ ] Page/Component: ...
- [ ] API connection: ...
- [ ] Route: ...

### FE TEST
- [ ] Component test: ...
```

### Optional sections — only when the US requires it:

| Section | When to add | Example |
|---------|-------------|---------|
| DOC | New technical concept, new guide, or ADR | US-002: auth flow guide, ADR-004 |
| DEVOPS | New GCP service, new secret, docker-compose change | US-001: SendGrid to Secret Manager |
| E2E | End of sprint — one per sprint, critical flow only | Sprint 2: login and role-based routing |

### Rule for DOC:
Add DOC when someone new to the codebase would need a written explanation. "I wrote an endpoint" → no DOC. "I introduced a new pattern (state machine, auth flow, soft delete)" → DOC needed.

### Rule for DEVOPS:
Add DEVOPS when any of the following change:
- A new GCP service is used
- A new secret is added to Secret Manager
- `docker-compose.yml` changes
- CI/CD pipeline changes

### Rule for E2E:
- One E2E issue per sprint, opened at the end of the sprint
- Covers only the most critical user journey introduced in that sprint
- Written with Playwright, must pass in CI

---

## GitHub Project Board Structure

| View | Filter | Purpose |
|------|--------|---------|
| `Epics` | `label:epic` | All epics — project overview |
| `Backlog` | `-label:epic` | All US and E2E issues across all sprints |
| `Sprint 2` | `label:sprint-2 -label:epic` | Sprint 2 working view |
| `Sprint 3` | `label:sprint-3 -label:epic` | Sprint 3 working view |
| ... | ... | ... |

**Working view:** Always use the current `Sprint X` view during development. It shows only 4-5 items (US + E2E) — no noise.

**How to set a filter in GitHub Projects:**
1. Open the view
2. Click the filter bar at the top
3. Type the filter (e.g. `label:sprint-2 -label:epic`)
4. Press Enter → click Save

---

## How to Push Issues to GitHub

For bulk issue creation, use the VS Code AI assistant.

**Important:** `gh` CLI must be called with its full path in VS Code terminal on Windows:
```
C:\Program Files\GitHub CLI\gh.exe
```

Running `bash script.sh` does not work — bash on Windows uses its own PATH and cannot find `gh`. Always use VS Code AI with PowerShell and the full `gh.exe` path.

**Prompt structure for VS Code AI:**
```
gh is installed at: C:\Program Files\GitHub CLI\gh.exe
Repository: aykutcihan/stepup

Run all commands using the full path "C:\Program Files\GitHub CLI\gh.exe".
Run in PowerShell terminal inside VS Code.
Do not ask for confirmation — execute all commands one by one.

[list of gh issue create / edit / close commands]
```

---

## Seed Data Strategy

Seed data is part of the BE section of each sprint's US — not a standalone story (except for Sprint 3 and 4 where it is explicitly tracked as US-022 and US-024 due to the data volume).

| Sprint | Seed update |
|--------|-------------|
| Sprint 2 | Users with hashed passwords |
| Sprint 3 | Departments, user-department assignments (US-022) |
| Sprint 4 | Templates and template tasks (US-024) |
| Sprint 5 | Plans and plan tasks in various states |
| Sprint 6 | Notification log entries |
| Sprint 7 | Final polish — realistic, idempotent, all states covered |

Command to run seeder locally:
```bash
docker-compose run --rm backend python -m seeder
```

---

## Definition of Done for a US

A US is Done when all of the following are true:
- All checkboxes in Sub-issues are checked
- All tests pass in CI pipeline
- PR is reviewed and merged to develop
- Acceptance criteria in the US issue are all checked off