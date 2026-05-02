# Commit Convention

All commits in this repository follow a strict format to keep history readable and traceable.

---

## Format

```
<type>(<scope>): <verb> <what>
```

---

## Types

| Type | When to use |
|------|-------------|
| `feat` | Feature code — model, endpoint, service, component, migration |
| `fix` | Bug fix |
| `test` | Test files only |
| `docs` | Markdown, guides, ADRs — no code |
| `chore` | Config, dependencies, tooling — no behavior change |
| `refactor` | Code restructure without behavior change |
| `ci` | GitHub Actions pipeline changes |

---

## Scope

| Scope | Rule | Example |
|-------|------|---------|
| `us-XXX` | Work tied to a specific user story — used with `feat`, `fix`, `test` | `feat(us-001):` |
| Domain | Not tied to a single US — used with `fix`, `refactor` | `fix(auth):` |
| *(empty)* | Project-wide changes — used with `docs`, `chore`, `ci` | `docs:` |

**Domain list for this project:**
`auth` · `user` · `db` · `email` · `api` · `docker` · `seed`

---

## Verbs

| Verb | When to use | Do not use when |
|------|-------------|-----------------|
| `add` | Adding a small, atomic piece to an existing structure (a field, a function, an env var) | Creating a new file from scratch |
| `create` | Creating a new file or entity from scratch (model, migration, component, page) | Modifying an existing file |
| `implement` | Building a complete behavior or flow that spans multiple files | A single-file change |
| `update` | Modifying something that already exists | Adding something new |
| `remove` | Deleting code, files, or config | — |
| `configure` | Setting up tooling, integrations, or secrets | — |
| `wire` | Connecting two existing pieces (service → endpoint, component → API call) | — |
| *(none)* | `fix` type only — describe what was broken, not the action | — |

---

## Rules

1. All lowercase, no trailing period
2. Subject line must not exceed 72 characters
3. `feat`, `fix`, `test`, `refactor` → scope is **required**
4. `docs`, `chore`, `ci` → scope is **optional**
5. `fix` type → skip the verb, describe what was broken or corrected

---

## Examples

```
feat(us-001): create invitation token model
feat(us-001): add expiry field to invitation table
feat(us-001): implement email sending via sendgrid
feat(us-001): wire invitation service to register endpoint
test(us-001): add unit tests for token expiry logic
test(us-001): add integration tests for invite endpoint
fix(us-001): handle expired token on registration
fix(auth): resolve null check on missing user session
refactor(db): extract base model to shared module
docs: add commit convention guide
chore: configure sendgrid api key in docker-compose
ci: add lint step to pull request workflow
```
