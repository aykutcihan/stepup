# Frontend Docker Setup

## Overview

The frontend runs in Docker during local development. This keeps the Node.js version and all dependencies consistent across machines.

---

## Our Dockerfile Explained

```dockerfile
FROM node:18-slim

WORKDIR /app

COPY apps/frontend/package.json ./package.json

RUN npm install

COPY apps/frontend .

EXPOSE 3000

CMD ["node_modules/.bin/vite", "--host"]
```

### Build context

The build context is the root of the monorepo (`.`), not `apps/frontend/`. This is set in `docker-compose.yml`:

```yaml
build:
  context: .
  dockerfile: apps/frontend/Dockerfile
```

This means `COPY apps/frontend/...` works — Docker can see the full monorepo structure during build.

### `FROM node:18-slim`

Node.js 18 LTS on a slim Debian base. `-slim` removes unnecessary system packages, keeping the image small (~200MB vs ~1GB for the full image).

### `COPY apps/frontend/package.json ./package.json`

Copy only `package.json` first, before copying any source code. This is Docker layer caching optimization:

```
Layer 1: COPY package.json    → changes only when dependencies change
Layer 2: RUN npm install      → skipped if layer 1 is cached
Layer 3: COPY apps/frontend . → always runs (code changes frequently)
```

If you copy all files first, every code change invalidates the `npm install` cache — reinstalling all packages on every build. Copying `package.json` first makes `npm install` cache-friendly.

### `RUN npm install`

Installs all dependencies inside the container.

**Why npm instead of pnpm?**

The project uses pnpm workspaces on the host machine (monorepo management). But inside Docker, pnpm's storage structure — symbolic links pointing to a virtual store (`.pnpm/` directory) — does not work reliably with Docker's anonymous volume mechanism.

npm creates a flat, self-contained `node_modules/` directory. No symlinks to an external store. This works reliably in Docker containers.

The choice of package manager is a developer workflow concern. The running container only needs the packages installed — it does not care how they were installed.

### `COPY apps/frontend .`

Copies all frontend source files into the container's `/app`. This runs after `npm install`, so it does not overwrite `node_modules/`.

Note: `.dockerignore` at the root excludes `**/node_modules` from the build context, preventing the host's `node_modules/` from being copied into the container.

### `CMD ["node_modules/.bin/vite", "--host"]`

Starts the Vite development server.

`--host` makes Vite listen on all network interfaces (`0.0.0.0`), not just localhost. Without this, the container's Vite server would not be reachable from the host machine's browser.

The binary path `node_modules/.bin/vite` is relative to `/app` (the WORKDIR). It resolves to `/app/node_modules/.bin/vite`.

---

## docker-compose.yml — Frontend Service

```yaml
frontend:
  build:
    context: .
    dockerfile: apps/frontend/Dockerfile
  container_name: stepup-frontend
  ports:
    - "3000:3000"
  volumes:
    - ./apps/frontend:/app
    - /app/node_modules
  depends_on:
    - backend
```

### `ports: "3000:3000"`

Maps host port 3000 to container port 3000. Vite uses port 5173 by default but the container exposes 3000 as a stable convention. The port mapping can be adjusted without changing the Dockerfile.

### Volumes: Two-Volume Pattern

```yaml
- ./apps/frontend:/app          # bind mount: source code
- /app/node_modules             # anonymous volume: dependencies
```

**Bind mount** (`./apps/frontend:/app`) — links the host's `apps/frontend/` directory to the container's `/app`. When you save a file in VS Code, the container sees the change immediately. Vite's HMR (Hot Module Replacement) picks it up and reloads the browser.

**Anonymous volume** (`/app/node_modules`) — a Docker-managed storage area at `/app/node_modules`. This overrides the `node_modules` from the bind mount.

The bind mount would otherwise replace `/app` with the host's directory, which does not have `node_modules/` (because we use `.dockerignore`). The anonymous volume provides the `node_modules/` that was installed during the Docker build.

This pattern is the standard solution for keeping node_modules inside the container while mounting source code from the host.

### `depends_on: backend`

The frontend container starts after the backend container. Does not wait for the backend to be healthy — only waits for the container to start.

---

## .dockerignore

```
**/node_modules
**/.git
**/__pycache__
...
```

Excludes `node_modules` from the Docker build context. Without this:

1. Docker would try to copy `apps/frontend/node_modules/` into the container during `COPY apps/frontend .`
2. pnpm's node_modules contains thousands of symbolic links
3. Docker would fail trying to overwrite directories with symlinks (and vice versa)
4. Build times would be massively longer

Always exclude `node_modules` from the Docker build context.
