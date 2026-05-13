# 13 Docker Commands

> I only add commands here when I actually use them and understand why.
> This is my personal reference, not a complete Docker manual.

---

## docker-compose up

```powershell
docker-compose up           # start all services, show logs in terminal
docker-compose up -d        # start all services in background (detached)
docker-compose up -d db     # start only the db service
docker-compose up backend   # start only the backend service
```

**What it does:** Starts the containers defined in `docker-compose.yml`.
`-d` = detached mode — runs in background, terminal stays free.

**When I used it:**
```powershell
# Start only database (EAP project was using port 5432, so we start only db)
docker-compose up -d db
```

---

## docker-compose build

```powershell
docker-compose build backend    # rebuild the backend image
docker-compose build            # rebuild all images
```

**What it does:** Rebuilds the Docker image from the Dockerfile.
Must run after changing `requirements.txt`, `Dockerfile`, or any file
that is part of the image build process.

**When I used it:**
```powershell
# After adding psycopg2-binary to requirements.txt
docker-compose build backend
```

**Important:** Changes to application code (`.py` files) do NOT require a rebuild
because of the bind mount volume (`./apps/backend:/app`).
Code changes are reflected immediately. Only dependency or Dockerfile changes need a rebuild.

---

## docker-compose run

```powershell
docker-compose run --rm backend <command>
```

**What it does:** Runs a one-off command inside a new container.
`--rm` = remove the container after the command finishes (no leftover containers).

**When I used it:**
```powershell
# Generate Alembic migration
docker-compose run --rm backend alembic revision --autogenerate -m "create users table"

# Apply migrations to database
docker-compose run --rm backend alembic upgrade head

# Roll back last migration
docker-compose run --rm backend alembic downgrade -1
```

**Difference from docker-compose exec:**
- `run` → starts a NEW container to run the command
- `exec` → runs the command inside an ALREADY RUNNING container

---

## docker-compose restart

```powershell
docker-compose restart frontend     # restart one service
docker-compose restart              # restart all services
```

**What it does:** Stops and restarts the container using the same image.
Does not rebuild the image, does not reinstall `node_modules`.

**When to use vs alternatives:**

| Situation | Command |
|-----------|---------|
| Process crashed, volume mount out of sync, container stuck | `docker-compose restart frontend` |
| `package.json` changed (new dependency added) | `docker-compose up --build frontend` |
| `Dockerfile` changed | `docker-compose up --build frontend` |
| Full reset (clear all data) | `docker-compose down -v` then `up --build` |

**When we used it:** Vite was failing to resolve `@/pages/RegisterPage` with a 500 error.
The container had started in a bad state — `restart` fixed it without a full rebuild.

---

## docker-compose down

```powershell
docker-compose down           # stop and remove containers
docker-compose down -v        # also remove volumes (deletes database data!)
```

**What it does:** Stops all running containers and removes them.
`-v` also removes volumes — use with caution, this deletes all database data.

**When to use:**
```powershell
docker-compose down     # normal shutdown, data preserved
docker-compose down -v  # full reset, start fresh (DELETES DATA)
```

---

## docker-compose logs

```powershell
docker-compose logs             # show logs from all services
docker-compose logs backend     # show logs from backend only
docker-compose logs -f backend  # follow logs in real time (like tail -f)
```

**What it does:** Shows the output (stdout/stderr) from containers.
`-f` = follow — keeps streaming new log lines as they appear.

**When I used it:** To debug errors when the backend failed to start.

---

## docker ps

```powershell
docker ps           # list running containers
docker ps -a        # list all containers (including stopped ones)
```

**What it does:** Shows which containers are currently running.

Output includes: Container ID, Image name, Port mappings, Container name.

**When I used it:**
```powershell
docker ps
# Saw that port 5432 was taken by EAP project (db-postgres container)
# Changed stepup db port to 5433
```

---

## docker exec

```powershell
docker exec -it <container-name> <command>
```

**What it does:** Runs a command inside an already running container.
`-it` = interactive terminal (needed for commands that require input).

**When I used it:**
```powershell
# Connect to database and check if tables were created
docker exec -it stepup-db psql -U stepup -d stepup_db -c "\dt"

# Output:
#  Schema |      Name       | Type  | Owner
# --------+-----------------+-------+--------
#  public | alembic_version | table | stepup
#  public | users           | table | stepup
```

---

## docker stop

```powershell
docker stop <container-name>
docker stop db-postgres eap-backend-api   # stop multiple containers
```

**What it does:** Gracefully stops a running container.

**When I used it:** EAP project containers were using port 5432 and 8000.
Stopped them temporarily to free up ports.

---

## Port Mapping (Important Concept)

```yaml
ports:
  - "5433:5432"
```

Format: `"HOST_PORT:CONTAINER_PORT"`

- Left (5433) = port on your computer
- Right (5432) = port inside the container

```
Your computer → localhost:5433 → Docker → container:5432 → PostgreSQL
```

**Why we use 5433:** EAP project was already using 5432.
Mapping to 5433 on the host avoids the port conflict.

---

## Backend-Specific Commands

```powershell
# Run backend tests
docker-compose run --rm backend pytest

# Apply database migrations
docker-compose run --rm backend alembic upgrade head

# Seed the database with initial data (HR Admin user)
# Creates: admin@stepup.com / Admin1234!
docker-compose run --rm backend python scripts/seed.py
```

---

## E2E Tests

```powershell
# Start the full stack first
docker-compose up -d db backend frontend

# Run E2E tests (builds playwright container on first run)
docker-compose run --rm playwright sh -c "pnpm install && pnpm e2e"
```

---

## Frontend-Specific Commands

```powershell
# First time or after Dockerfile/package.json changes
docker-compose up frontend --build

# Subsequent runs (no rebuild needed)
docker-compose up frontend

# Force a clean rebuild (clears Docker cache)
docker-compose build --no-cache frontend
docker-compose up frontend

# Full reset (removes volumes — node_modules rebuilt from scratch)
docker-compose down -v
docker-compose up frontend --build

# Run frontend tests inside container
docker-compose run --rm frontend node_modules/.bin/vitest run --config vitest.config.ts --passWithNoTests

# View frontend logs
docker-compose logs -f frontend

# Regenerate TypeScript types from BE OpenAPI spec (run after BE schema changes)
docker-compose run --rm frontend node_modules/.bin/openapi-typescript http://backend:8000/openapi.json -o src/types/api.ts
```

**When to rebuild vs when not to:**

| Change | Action needed |
|--------|--------------|
| Source code (`.tsx`, `.ts`, `.css`) | Nothing — bind mount reflects instantly |
| `package.json` (add/remove dependency) | `docker-compose up frontend --build` |
| `Dockerfile` | `docker-compose up frontend --build` |
| Broken `node_modules` in container | `docker-compose down -v` then `--build` |

---

## Common Issues & Solutions

| Issue | Solution |
|---|---|
| Port already in use | Change host port in docker-compose.yml (left side of mapping) |
| Changes not reflected | For dependency changes: `docker-compose build`. For code changes: automatic via volume. |
| Container keeps restarting | Check logs: `docker-compose logs backend` |
| Database data lost | Check if you ran `docker-compose down -v` — volumes were deleted |