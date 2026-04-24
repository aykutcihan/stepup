# Git Commands — Learned As I Go

> I only add commands here when I actually use them and understand why.
> This is my personal reference, not a complete git manual.

---

## git clone

```powershell
git clone <url>
```

**What it does:** Downloads a remote repository to your computer.
Creates a new folder with the repo name automatically.

**When I used it:** To download the stepup repo from GitHub to `C:\Dev\stepup`.

```powershell
cd C:\Dev
git clone https://github.com/aykutcihan/stepup.git
```

---

## git status

```powershell
git status
```

**What it does:** Shows what has changed since the last commit.
- Red = changed but not staged yet
- Green = staged, ready to commit
- "nothing to commit" = everything is clean

**When I used it:** Before every commit, to see exactly what will be committed.

---

## git branch

```powershell
git branch                  # list all local branches
git checkout -b <name>      # create new branch and switch to it
git checkout <name>         # switch to existing branch
git branch -d <name>        # delete a branch
```

**What it does:** Manages branches. We use one branch per issue — this keeps
each feature isolated. If something breaks, it does not affect other branches.

**Our branch strategy:**
```
main      → production, never commit directly
develop   → integration, merge features here first
feature/  → one branch per issue (feature/us-001-register-user)
fix/      → one branch per bug fix (fix/pytest-no-tests)
```

**When I used it:** Every time I start a new issue, I create a feature branch from develop.

```powershell
git checkout develop
git checkout -b feature/us-006-monorepo-setup
```

---

## git add, commit, push

```powershell
git add .                      # stage all changes
git add <file>                 # stage a specific file
git commit -m "type: message"  # save staged changes with a message
git push origin <branch>       # send commits to GitHub
```

**What it does:** The core workflow. Every change goes through these 3 steps.

**Commit message types I use:**
```
feat    → new feature
fix     → bug fix
chore   → setup, config, tooling
docs    → documentation only
test    → adding or updating tests
```

**When I used it:** After finishing work on each issue, before opening a PR.

```powershell
git add .
git commit -m "chore: add Docker configuration and docker guide"
git push origin feature/us-007-docker-setup
```

---

## git pull

```powershell
git pull origin <branch>
```

**What it does:** Fetches changes from GitHub and merges them into your current branch.
Always run this after switching to develop — someone (or a PR merge) may have updated it.

**When I used it:** After merging a PR on GitHub, to sync local develop with remote develop.

```powershell
git checkout develop
git pull origin develop
```

---

## git merge

```powershell
git merge <branch>
```

**What it does:** Brings changes from another branch into the current branch.
We usually merge via Pull Requests on GitHub — not directly in terminal.
But sometimes useful locally to sync branches.

**When I used it:** To bring develop changes into a feature branch.

```powershell
git checkout feature/us-010-database-schema
git merge develop
```

---

## git log

```powershell
git log --oneline          # compact commit history (one line per commit)
git log --oneline -5       # show only last 5 commits
git log --all --oneline -20  # show commits from ALL branches
```

**What it does:** Shows commit history. `--oneline` makes it readable.
Each line shows: `<hash> <message> (<branch>)`

**When I used it:** To check what was committed in the current branch,
and to find a specific commit hash for revert.

```powershell
git log --oneline -5
# 8cf8074 (HEAD -> feature/us-010) .
# fd1d0c9 Revert "Merge pull request #17..."
# 798a397 Merge pull request #17...
```

---

## git revert

```powershell
git revert <commit-hash> --no-edit           # revert a regular commit
git revert <commit-hash> -m 1 --no-edit      # revert a merge commit
```

**What it does:** Creates a new commit that undoes a previous commit.
Safe — it does not delete history, it adds a new "undo" commit.

**`-m 1`** is required when reverting a merge commit.
It tells git which "parent" to revert to (always use 1 for our case).

**`--no-edit`** skips the commit message editor — uses the default message.

**When I used it:** PR #17 accidentally reverted all our work. We used revert to undo that revert
and restore all 17 files.

```powershell
git revert 798a397 -m 1 --no-edit
git push origin develop
```

---

## git push (force not used — good practice)

> I never use `git push --force` on shared branches (develop, main).
> Force push rewrites history and can destroy other people's work.
> The only safe place for force push is on your own feature branch, before a PR is opened.

---

## gh issue

```powershell
gh issue view <number>   # show issue details (title, body, labels, assignee)
gh issue list            # list all issues in the repo
```

**What it does:** Reads GitHub issues directly from the terminal — no browser needed.
`view` shows the full issue: description, acceptance criteria, labels, who it's assigned to.
`list` shows all open issues with their numbers and titles at a glance.

**When I used it:** To check what a US requires before starting work, and to see which issues are still open.

```powershell
gh issue view 10         # show US-010 details
gh issue list            # list all open issues in aykutcihan/stepup
```