# 08 — GitHub Actions CI

## What is GitHub Actions?

Imagine this scenario:

```
You wrote code
You ran git push
Tests run automatically
If tests pass → deploy to GCP automatically
```

You do not have to do any of this manually.
GitHub Actions does it for you.

**GitHub Actions = an automated task runner**

When an event happens — like `git push` — GitHub Actions
runs the steps you defined, in order.

```
You: git push
GitHub Actions:
  1. Get the code
  2. Install Python
  3. Run tests
  4. Tests passed?
  5. Yes → deploy to GCP
  6. No  → stop, notify me
```

---

## 3 Core Concepts

### Workflow

The full automation plan. Defined in a `.yml` file inside `.github/workflows/`.

```
.github/
  workflows/
    ci.yml      ← this is the workflow file
```

Real world analogy:
```
Workflow = "Morning routine"
```

### Job

A group of tasks inside a workflow. Multiple jobs can run **in parallel**.

```
Workflow = "Morning routine"
  Job 1 = "Prepare breakfast"
  Job 2 = "Get ready"
```

Both jobs run at the same time — one prepares breakfast while the other gets dressed.

**Each job runs on a separate virtual machine** that GitHub creates fresh for every run.

### Step

Individual actions inside a job. Steps run **sequentially** — one must finish before the next starts.

```
Job 1 = "Prepare breakfast"
  Step 1: Get bread
  Step 2: Add cheese
  Step 3: Brew tea
```

### Summary

```
Workflow (ci.yml)
  └── Job 1: test-backend    ← runs in parallel
        └── Step 1: checkout code
        └── Step 2: install Python
        └── Step 3: pip install
        └── Step 4: run pytest
  └── Job 2: test-frontend   ← runs in parallel
        └── Step 1: checkout code
        └── Step 2: install Node.js
        └── Step 3: pnpm install
        └── Step 4: run pnpm test
```

---

## Why Two Jobs Instead of One?

With one job (sequential):
```
backend test (2 min) → frontend test (2 min) = 4 minutes total
```

With two jobs (parallel):
```
backend test (2 min)
                     = 2 minutes total
frontend test (2 min)
```

Half the time. As the project grows, this matters more.

---

## GitHub Actions vs Docker

They look similar — both use `.yml` files with services/jobs and steps.
But they serve different purposes:

| | Docker | GitHub Actions |
|---|---|---|
| Purpose | Run the application | Quality control |
| When | Local development, production | On every push / PR |
| What it does | Starts backend, frontend, database | Runs tests, lints code, deploys |
| File | `docker-compose.yml` | `.github/workflows/ci.yml` |

```
Docker          → "start the app and keep it running"
GitHub Actions  → "check if the code is correct"
```

---

## Our CI Workflow (ci.yml)

```yaml
name: CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]
```

### When does it run?

| Event | Branch | Runs? |
|---|---|---|
| push | feature/xxx | No |
| push | develop | Yes |
| push | main | Yes |
| pull_request | develop | Yes |
| pull_request | main | Yes |

**Why both develop and main?**

```
Our branch strategy:
  feature → develop → main

develop = integration branch (test environment)
main    = production (live on GCP)
```

If we only tested on `main`, errors would reach production before being caught.
By testing on `develop` too, errors are caught before they ever reach `main`.

---

## Jobs Explained

### test-backend job

```yaml
test-backend:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install dependencies
      working-directory: apps/backend
      run: |
        pip install --upgrade pip
        pip install pytest

    - name: Run tests
      working-directory: apps/backend
      run: pytest
```

| Line | Meaning |
|---|---|
| `runs-on: ubuntu-latest` | Run on GitHub's Ubuntu virtual machine |
| `uses: actions/checkout@v4` | GitHub's ready-made action — copies repo to virtual machine |
| `uses: actions/setup-python@v5` | GitHub's ready-made action — installs Python |
| `working-directory: apps/backend` | Run this step inside the `apps/backend` folder |
| `run: pytest` | Run all tests — if any fail, workflow fails |

### test-frontend job

```yaml
test-frontend:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: "18"

    - name: Install pnpm
      uses: pnpm/action-setup@v3
      with:
        version: 10

    - name: Install dependencies
      working-directory: apps/frontend
      run: pnpm install

    - name: Run tests
      working-directory: apps/frontend
      run: pnpm test
```

Same structure as backend — but uses Node.js and pnpm instead of Python and pip.

---

## What is `uses`?

```yaml
uses: actions/checkout@v4
```

GitHub has a marketplace of ready-made actions.
Instead of writing "how to install Python" from scratch,
you just say `uses: actions/setup-python@v5` and it handles everything.

```
uses: actions/checkout@v4        → clone the repo
uses: actions/setup-python@v5   → install Python
uses: actions/setup-node@v4     → install Node.js
uses: pnpm/action-setup@v3      → install pnpm
```

`@v4`, `@v5` = version of the action. Always pin to a version — never use `@latest`.

---

## What Happens on a PR

```
1. You open a PR: feature/us-001 → develop
2. GitHub Actions starts automatically
3. Two jobs run in parallel:
   - test-backend: runs pytest
   - test-frontend: runs pnpm test
4a. All tests pass → green checkmark on PR → can merge
4b. Any test fails → red X on PR → cannot merge until fixed
```

This is called **branch protection** — main and develop are protected,
no broken code can enter.

---

## File Location

```
stepup/
  .github/
    workflows/
      ci.yml    ← CI pipeline (this file)
```

GitHub automatically detects any `.yml` file inside `.github/workflows/`
and treats it as a workflow. No registration needed.