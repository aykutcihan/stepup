# Setup Log

## 2026-04-21

### What I did

#### 1. Project Planning
- Decided on project: Employee Onboarding Management Platform
- Project name decided: **StepUp**
- Created Product Vision document (v1.1) covering:
  - Vision statement and problem definition
  - 3 user roles: HR Admin, Manager, Employee
  - Core workflow: Assign → Complete → Approve
  - Task state machine (7 states)
  - Onboarding plan state machine (4 states)
  - Full tech stack decisions
  - Monorepo + GCP architecture
  - Database schema with indexes
  - Error handling strategy (centralized exceptions)
  - Frontend constants strategy
  - Logging strategy (GCP Cloud Logging)
  - Security approach (OWASP coverage table)
  - Testing strategy (unit + integration + E2E)
  - Sprint 1-6 roadmap
  - Out of scope list
  - Success metrics
  - Open questions & decisions

#### 2. GitHub Repository Setup
- Created GitHub repository: `aykutcihan/stepup`
  - Repository name: stepup
  - Description: Employee onboarding management platform
  - Visibility: Public
  - README: On
  - .gitignore: Python
  - License: None
- Created GitHub Projects board: StepUp Board
  - Default had 3 columns: Todo, In Progress, Done
  - Manually added 4th column: In Review
  - Final order: Todo → In Progress → In Review → Done

#### 3. GitHub CLI Setup
- Downloaded and installed GitHub CLI (gh v2.90.0)
  from https://cli.github.com
- Connected CLI to aykutcihan account:
  ```
  gh auth login
  ```
  - Selected: GitHub.com, HTTPS, Yes, Login with browser
- Added missing scopes:
  ```
  gh auth refresh -s read:project
  gh auth refresh -s project
  ```

#### 4. Labels Created via GitHub CLI
```powershell
gh label create "sprint-1" --repo aykutcihan/stepup --color "0075ca"
gh label create "sprint-2" --repo aykutcihan/stepup --color "e4e669"
gh label create "sprint-3" --repo aykutcihan/stepup --color "d93f0b"
gh label create "backend"  --repo aykutcihan/stepup --color "1d76db"
gh label create "frontend" --repo aykutcihan/stepup --color "e99695"
gh label create "devops"   --repo aykutcihan/stepup --color "0e8a16"
gh label create "database" --repo aykutcihan/stepup --color "5319e7"
gh label create "security" --repo aykutcihan/stepup --color "b60205"
gh label create "documentation" --repo aykutcihan/stepup --color "c5def5"
```
> Note: "documentation" label already existed by default.

#### 5. Sprint 1 Issues Created via GitHub CLI
Created 11 issues using `gh issue create`:

| # | Issue |
|---|---|
| #1  | US-001: HR Admin can register a new user account |
| #2  | US-002: User can log in with email and password |
| #3  | US-003: User can refresh access token |
| #4  | US-004: User can log out |
| #5  | US-005: HR Admin can create and manage departments |
| #6  | US-006: Setup monorepo structure (Turborepo + pnpm) |
| #7  | US-007: Setup Docker + docker-compose |
| #8  | US-008: Setup GCP project |
| #9  | US-009: Setup GitHub Actions CI pipeline |
| #10 | US-010: Database schema + Alembic migration |
| #11 | US-011: Seed data — minimum dataset |

Added all 11 issues to StepUp Board using for loop:
```powershell
for ($i = 1; $i -le 11; $i++) {
    gh project item-add 5 --owner aykutcihan --url "https://github.com/aykutcihan/stepup/issues/$i"
}
```

#### 6. Local Environment Setup
- Checked Node.js version: v24.13.0 (already installed)
- Installed pnpm globally:
  ```
  npm install -g pnpm
  ```
- **Issue:** pnpm not recognized after install (PATH problem)
- Temporary fix in PowerShell:
  ```
  $env:PATH += ";$env:APPDATA\npm"
  ```
- Permanent fix via PowerShell profile:
  ```
  New-Item -Path $PROFILE -ItemType File -Force
  notepad $PROFILE
  ```
  Added line: `$env:PATH += ";$env:APPDATA\npm"`
- Same PATH issue occurred in VS Code terminal — fixed with same profile approach
- pnpm version confirmed: 10.33.0

#### 7. Repository Cloned and Opened
```powershell
cd C:\Dev
git clone https://github.com/aykutcihan/stepup.git
cd stepup
code .
```

#### 8. Docs Folder Structure Created
```powershell
mkdir docs
mkdir docs\adr
New-Item docs\product-vision.md -ItemType File
New-Item docs\setup-log.md -ItemType File
New-Item docs\adr\ADR-001-fastapi.md -ItemType File
New-Item docs\adr\ADR-002-gcp-stack.md -ItemType File
New-Item docs\adr\ADR-003-state-management.md -ItemType File
New-Item docs\adr\ADR-004-httonly-cookie.md -ItemType File
New-Item docs\adr\ADR-005-monorepo-turborepo.md -ItemType File
New-Item docs\adr\ADR-006-api-versioning.md -ItemType File
New-Item docs\adr\ADR-007-structured-logging.md -ItemType File
```

---

### Why These Decisions

| Decision | Reason |
|---|---|
| GitHub Projects over Jira | Employers see everything in one place: code, sprints, PRs, commits |
| pnpm over npm | Faster installs, better monorepo support, less disk usage |
| docs/ folder over GitHub Wiki | Versioned with code, visible to employers when browsing repo |
| C:\Dev folder | Dedicated development folder, keeps projects isolated and organized |

---

### What I Learned
- `gh auth login` connects GitHub CLI to GitHub account
- GitHub CLI needs specific scopes for different features:
  - `read:project` — for listing projects
  - `project` — for adding items to board
- `gh label create` creates labels from terminal
- `gh issue create` creates issues from terminal
- `gh project item-add` adds issues to project board
- PowerShell for loop syntax: `for ($i = 1; $i -le 11; $i++) { ... }`
- `code .` opens current folder in VS Code
- PowerShell `$PROFILE` sets persistent environment variables
- Each project in `C:\Dev` is isolated, cloning is safe
- pnpm PATH issue on Windows is common, fixed via profile

---

### Issues & Solutions

| Issue | Solution |
|---|---|
| pnpm not recognized after install | Added npm path to `$PROFILE` |
| gh project commands failing | Added `read:project` and `project` scopes via `gh auth refresh` |
| VS Code terminal pnpm not found | Same `$PROFILE` fix |

## 2026-04-22

### What I did

#### GCP Project Setup (US-008)

**APIs Enabled:**
- Cloud Run Admin API
- Cloud SQL Admin API
- Secret Manager API
- Cloud Build API

**Cloud SQL:**
- Instance: stepup-db (PostgreSQL 18)
- Region: europe-west4 (Netherlands)
- Public IP: 34.32.215.164
- Database: stepup_db
- User: stepup_user

**Secret Manager:**
- DATABASE_URL
- JWT_SECRET_KEY
- SENDGRID_API_KEY

### What I learned
- GCP APIs are disabled by default — must enable before use
- Cloud SQL is a managed PostgreSQL on GCP servers
- Secret Manager stores sensitive values securely
- Never put secrets in .env files that go to GitHub