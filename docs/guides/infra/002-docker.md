# Docker

## The Problem Docker Solves

"It works on my machine but not on the server."

This is the most classic problem in software development.
The reason: your machine has Python 3.11, the server has Python 3.9.
Your machine has PostgreSQL 15, the server has PostgreSQL 13.
Different environments, different behavior.

**Docker solves this.**

---

## What is Docker?

Docker = a system for putting your application in a box.

This box is called a **container**. Inside the container:
- Your application code
- The exact Python version your app needs
- All required libraries
- Necessary system tools

Everything together, isolated, portable.

Run this container on any computer, any server — the result is always the same.

---

## Real World Analogy

Think of shipping containers:
- Before containers: every product was loaded differently — messy, inefficient
- With containers: every product goes into a standard box
- The same crane lifts every box, the same ship carries every box

Docker containers work the same way — whatever the application,
it goes into a standard box.

---

## 3 Core Concepts

### 1. Dockerfile

Dockerfile = the instruction manual for building a container.
"What does this application need to run?" — this file answers that question.

```dockerfile
FROM python:3.11-slim   # start from a ready-made Python 3.11 environment
WORKDIR /app            # go into the /app folder
COPY requirements.txt . # copy the dependency list
RUN pip install -r requirements.txt  # install libraries
COPY . .                # copy all the code
CMD ["uvicorn", "app.main:app"]  # start the application
```

No Dockerfile = no container. Every app needs its own Dockerfile.

### 2. Image

Image = the ready-made template built from a Dockerfile.

```
Dockerfile  →  docker build  →  Image
(recipe)                        (ready template)
```

Images are immutable — built once, used everywhere.
Docker Hub has thousands of ready-made images:

```
python:3.11-slim   → Python installed
postgres:15        → PostgreSQL installed
node:18-slim       → Node.js installed
```

We take these as a base and add our own code on top.

### 3. Container

Container = a running instance created from an image.

```
Image  →  docker run  →  Container
(template)               (running application)
```

You can run multiple containers from the same image:

```
backend image → container 1 (port 8000)
backend image → container 2 (port 8001)
backend image → container 3 (port 8002)
```

This is scaling — when traffic increases, open more containers.

### Summary

```
Dockerfile  →  recipe
Image       →  prepared but not yet opened box
Container   →  opened, running box
```

Food analogy:
```
Dockerfile  =  recipe card
Image       =  prepared but uncooked meal
Container   =  plated, ready-to-eat meal
```

---

## Our Project: 3 Containers

```
Backend container   (FastAPI)     → port 8000
Frontend container  (React)       → port 3000
Database container  (PostgreSQL)  → port 5432
```

3 separate containers, but they can talk to each other.

### How They Communicate

This is where **docker-compose** comes in.

docker-compose = the manager that runs all 3 containers together.

```
docker-compose up
```

This single command:
- Starts the database container
- Starts the backend container
- Starts the frontend container
- Sets up networking so they can talk to each other

### Communication Flow

```
Frontend → "Backend, give me this user's tasks"
Backend  → "OK, asking the database"
Database → "Here is the data"
Backend  → "Frontend, here you go"
Frontend → "Showing on screen"
```

This communication happens over Docker's internal network.
docker-compose sets this up automatically.

---

## Backend Dockerfile Explained

```dockerfile
FROM python:3.11-slim
```
Download the `python:3.11-slim` image from Docker Hub.
`-slim` = smaller size (~130MB vs ~900MB), unnecessary files removed.
Compatible with most libraries — better choice than `-alpine`.

```dockerfile
WORKDIR /app
```
Set `/app` as the working directory inside the container.
All following commands run inside this folder.
Like doing `cd /app` on your computer.

```dockerfile
COPY requirements.txt .
```
Copy `requirements.txt` into the container's `/app` folder.
We copy this BEFORE the code — this is intentional (see Cache section below).

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
Install all libraries inside the container.
`--no-cache-dir` = do not keep installation cache, keeps image size small.

```dockerfile
COPY . .
```
Copy all application code into the container.
First `.` = your computer's folder, second `.` = container's `/app`.

```dockerfile
EXPOSE 8000
```
"This container uses port 8000." Informational — tells docker-compose which port to use.

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```
Command to run when the container starts.
- `--host 0.0.0.0` = allow connections from outside the container
- `--reload` = automatically restart when code changes

---

## Frontend Dockerfile Explained

```dockerfile
FROM node:18-slim
```
Frontend is React — needs Node.js, not Python.

```dockerfile
COPY apps/frontend/package.json ./package.json
```
Copy only `package.json` first. The build context is the monorepo root (`.`), so the path includes `apps/frontend/`. Copied before the code for Docker cache optimization — `npm install` is skipped on rebuilds when dependencies have not changed.

```dockerfile
RUN npm install
```
Install all frontend libraries inside the container.

We use `npm` instead of `pnpm` in Docker. pnpm's storage structure uses symbolic links pointing to a virtual store (`.pnpm/` directory). This does not work reliably with Docker's anonymous volume mechanism. npm creates a flat, self-contained `node_modules/` — more reliable inside containers.

```dockerfile
COPY apps/frontend .
```
Copy all frontend source files after installing dependencies.

```dockerfile
CMD ["node_modules/.bin/vite", "--host"]
```
Start the Vite development server. `--host` makes Vite listen on all interfaces so the browser on the host machine can reach it. The binary path is relative to WORKDIR (`/app`).

For a full explanation of the frontend Docker setup including volumes, `.dockerignore`, and the two-volume pattern, see `docs/guides/tutorials/frontend/006-docker.md`.

---

## docker-compose.yml Explained

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: stepup
      POSTGRES_PASSWORD: stepup123
      POSTGRES_DB: stepup_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

- `image: postgres:15` → use ready-made PostgreSQL image, no Dockerfile needed
- `environment` → database username, password, database name
- `ports: "5432:5432"` → left = your computer's port, right = container's port
- `volumes` → save database data permanently (see Volumes section)

```yaml
  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://stepup:stepup123@db:5432/stepup_db
    depends_on:
      - db
```

- `build` → no ready-made image, build from our Dockerfile
- `DATABASE_URL` → how backend connects to database. Notice `@db` — `db` is the service name, Docker resolves it automatically
- `depends_on: db` → start database first, then start backend

```yaml
  frontend:
    volumes:
      - ./apps/frontend:/app
      - /app/node_modules
    depends_on:
      - backend
```

- `volumes: /app/node_modules` → keep node_modules inside container, do not mix with your computer's files
- `depends_on: backend` → start backend first, then start frontend

### Start Order

```
db starts → backend starts → frontend starts
```

---

## Volumes

### The Problem Without Volumes

When a container stops, everything inside it is deleted.

```
PostgreSQL container running
100 users registered
Container stopped
→ 100 users deleted, everything gone
```

This is a disaster. The database resets every time it stops.

### Volume = Persistent Storage

A volume is a storage area that exists outside the container.
Even if the container stops, the data stays there.

```
PostgreSQL container running
100 users registered → written to volume
Container stopped
Container started again
→ 100 users still there, read from volume
```

### Two Types of Volumes We Use

**1. Named volume — for database:**
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```
`postgres_data` = a storage area managed by Docker.
You do not need to know where it is — Docker handles it.
Database data stays here permanently.

**2. Bind mount — for code:**
```yaml
volumes:
  - ./apps/backend:/app
```
Links your computer's `./apps/backend` folder to the container's `/app` folder.

- You write code in VS Code
- Save the file
- Container sees it immediately, auto-reloads
- No need to restart the container

### Summary

```
Named volume  → database data must not be lost
Bind mount    → code changes reflect in container instantly
```

---

## Docker Cache Optimization

Why do we copy `requirements.txt` BEFORE copying the code?

```dockerfile
COPY requirements.txt .        ← step 1
RUN pip install -r requirements.txt  ← step 2
COPY . .                       ← step 3
```

Docker builds images layer by layer. Each step is a layer.
If a layer has not changed, Docker uses the cached version.

```
Day 1: requirements.txt copied → pip install (2 minutes) → code copied
Day 2: only code changed       → requirements.txt cached → pip install SKIPPED → code copied
```

If we copied the code first, every code change would trigger `pip install` again — 2 minutes every time.
By copying `requirements.txt` first, `pip install` only runs when dependencies change.

---

## Build Context and Python Imports

When Docker builds the backend, `context: ./apps/backend` tells it:
> "Go into this folder and take everything inside it."

The folder name `apps/backend/` does not go into the container — only its contents do.

```
Host machine:                Container:
apps/backend/           →    /app/
    app/                →        app/
        models/         →            models/
        enums/          →            enums/
    alembic/            →        alembic/
    requirements.txt    →        requirements.txt
```

Python starts from `/app` inside the container. It sees `app/` as a package — not `apps/`, not `backend/`.

This is why imports are written as:
```python
from app.enums.user_role import UserRole   # correct — /app/app/enums/user_role.py
from apps.backend.app.enums...             # wrong — no "apps" folder exists in container
```

The bind mount confirms the same:
```yaml
volumes:
  - ./apps/backend:/app   # apps/backend/ contents → mounted at /app
```

`apps/backend/` on your machine = `/app` in the container. The name is gone, only the contents matter.

---

## Common Docker Commands

```powershell
docker-compose up           # start all containers
docker-compose up -d        # start in background (detached)
docker-compose down         # stop all containers
docker-compose logs         # see all logs
docker-compose logs backend # see backend logs only
docker-compose build        # rebuild images
docker ps                   # list running containers
docker images               # list all images
```

---

## In Plain Terms

```
Dockerfile     =  recipe for one container
Image          =  prepared box, ready to use
Container      =  opened box, running application
docker-compose =  manager that runs all boxes together
Volume         =  permanent storage outside the box
```

Our project in one picture:
```
docker-compose up
       ↓
┌──────────────────────────────────┐
│  Docker Network                  │
│                                  │
│  [db:5432]  ←→  [backend:8000]  │
│                       ↑          │
│              [frontend:3000]     │
└──────────────────────────────────┘
       ↓
localhost:3000 → StepUp is running
```