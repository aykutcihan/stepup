# Git Commands Reference

## Basic Workflow

```powershell
git status                   # show changed files
git add .                    # stage all changes
git add <file>               # stage specific file
git commit -m "message"      # commit staged changes
git push                     # push to remote (GitHub)
git pull                     # pull latest from remote
```

---

## Branching

```powershell
git branch                   # list all branches
git branch <name>            # create new branch
git checkout <name>          # switch to branch
git checkout -b <name>       # create and switch in one step
git merge <name>             # merge branch into current
git branch -d <name>         # delete branch
```

---

## Our Branch Strategy

```
main            → production ready code, never commit directly
develop         → integration branch
feature/xxx     → one branch per issue

Examples:
feature/us-001-register-user
feature/us-006-monorepo-setup
feature/us-010-database-schema
```

---

## Feature Branch Workflow (how we work)

```powershell
# 1. Always start from latest main
git checkout main
git pull

# 2. Create feature branch for the issue
git checkout -b feature/us-006-monorepo-setup

# 3. Work on code...

# 4. Commit regularly with meaningful messages
git add .
git commit -m "chore: add turborepo configuration"

# 5. Push branch to GitHub
git push origin feature/us-006-monorepo-setup

# 6. Open Pull Request on GitHub
#    → Move issue card to: In Review

# 7. Merge PR on GitHub
#    → Move issue card to: Done

# 8. Clean up local branch
git checkout main
git pull
git branch -d feature/us-006-monorepo-setup
```

---

## Commit Message Format

```
type: short description (max 72 chars)

Types:
feat      → new feature
fix       → bug fix
docs      → documentation only
chore     → setup, config, tooling, no logic
test      → adding or updating tests
refactor  → code change, no new feature or fix
style     → formatting, whitespace, no logic change
```

### Examples

```
feat: add JWT authentication endpoint
feat: implement task state machine
fix: correct token expiry calculation
fix: handle missing refresh token gracefully
docs: update setup log for 2026-04-21
docs: add ADR-001 FastAPI decision
chore: setup turborepo monorepo structure
chore: add docker-compose configuration
test: add unit tests for task state machine
test: add integration tests for auth endpoints
refactor: extract email logic into notification service
```

---

## Useful Commands

```powershell
git log --oneline            # compact commit history
git log --oneline --graph    # visual branch history
git diff                     # show unstaged changes
git diff --staged            # show staged changes
git stash                    # temporarily save changes
git stash pop                # restore stashed changes
git reset HEAD <file>        # unstage a file
git remote -v                # show remote URLs
```

---

## Quick Reference Card

| Goal | Command |
|---|---|
| See what changed | `git status` |
| Stage everything | `git add .` |
| Commit | `git commit -m "type: message"` |
| Push to GitHub | `git push` |
| Get latest code | `git pull` |
| New feature branch | `git checkout -b feature/us-xxx-name` |
| Switch branch | `git checkout <branch>` |
| See all branches | `git branch` |
| Delete branch | `git branch -d <branch>` |
| See commit history | `git log --oneline` |