# Environment Setup

## Overview

Environment variables are split across three files:

| File | Purpose | Git |
|------|---------|-----|
| `.env` | Real values for local development | Ignored |
| `.env.example` | Template showing required variables | Committed |
| `docker-compose.yml` | References variables via `${VAR_NAME}` | Committed |

## Getting Started

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

## Variables

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | PostgreSQL database name |
| `DATABASE_URL` | Full async database connection string |
| `FRONTEND_URL` | Frontend base URL (e.g. http://localhost:3000) |
| `SENDGRID_API_KEY` | SendGrid API key for email delivery |
| `SENDGRID_FROM_EMAIL` | Sender email address |
| `JWT_SECRET_KEY` | Secret key used to sign JWT tokens |

## How Docker Compose resolves variables

When you run `docker compose up`, Docker Compose automatically reads the `.env` file in the same directory and resolves `${VAR_NAME}` references. No import or configuration needed — it works by convention.

The chain:
```
.env → Docker Compose → container environment → pydantic Settings
```

`pydantic-settings` (`BaseSettings`) reads the container's environment variables at startup. If a required variable is missing, the app fails to start immediately — no silent `None` values.

## Notes

- Never commit `.env` — it is listed in `.gitignore`
- In production, real values come from GCP Secret Manager
- `JWT_SECRET_KEY` must be a strong random string in production
