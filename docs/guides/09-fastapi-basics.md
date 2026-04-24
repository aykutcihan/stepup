# 09 — FastAPI Basics

## What is FastAPI?

FastAPI is a Python framework for building REST APIs.
Alternative to Django and Flask.

---

## Why We Chose FastAPI

| Framework | Problem |
|---|---|
| Django | Too large — ORM, templates, admin all included. We only need an API. |
| Flask | Too minimal — no validation, no docs, everything manual. |
| FastAPI | Just right — automatic Swagger, Pydantic validation, async support. |

---

## Our main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StepUp API",
    description="Employee onboarding management platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "stepup-backend"}
```

---

## FastAPI Instance

```python
app = FastAPI(
    title="StepUp API",
    docs_url="/docs",
    redoc_url="/redoc",
)
```

| Parameter | Purpose |
|---|---|
| `title` | Shows in Swagger UI header |
| `docs_url` | Where Swagger UI is available → `localhost:8000/docs` |
| `redoc_url` | Alternative API docs → `localhost:8000/redoc` |

FastAPI automatically generates interactive API documentation from your code.
No extra work needed — just run the app and go to `/docs`.

---

## CORS Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### What is CORS?

Browser security rule. When the frontend on `localhost:3000` sends a request
to the backend on `localhost:8000`, the browser asks:
"Is this allowed?" CORS answers that question.

Without CORS configured correctly:
```
Frontend → GET http://localhost:8000/users
Browser  → Blocked! Cross-origin request not allowed.
```

With CORS configured:
```
Frontend → GET http://localhost:8000/users
Browser  → Allowed (origin is in the whitelist)
Backend  → Returns data
```

### Our CORS settings

| Setting | Value | Meaning |
|---|---|---|
| `allow_origins` | `["http://localhost:3000"]` | Only frontend dev server is allowed |
| `allow_credentials` | `True` | Allow cookies (needed for HttpOnly JWT cookies) |
| `allow_methods` | `["*"]` | Allow all HTTP methods (GET, POST, PUT, DELETE) |
| `allow_headers` | `["*"]` | Allow all headers |

In production, `allow_origins` will be set to the real Firebase Hosting URL.

---

## Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "stepup-backend"}
```

### Why does this exist?

GCP Cloud Run calls this endpoint to check if the application is running.
If no response comes back → Cloud Run restarts the container.

It also serves as a quick sanity check:
```
curl http://localhost:8000/health
→ {"status": "ok", "service": "stepup-backend"}
```

If you get this response, the backend is running correctly.

---

## How to Run

```powershell
# Start all services
docker-compose up

# Backend only
docker-compose up backend

# Access Swagger UI
# → http://localhost:8000/docs
```

---

## YAGNI Applied

`main.py` currently only has:
- App initialization
- CORS middleware
- Health check

No routers, no database connections, no authentication — yet.
Each will be added when the corresponding feature is implemented.