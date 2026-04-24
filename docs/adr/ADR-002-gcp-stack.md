# ADR-002: GCP as Cloud Infrastructure

**Date:** 2026-04-22
**Status:** Accepted

---

## Context

StepUp needs a cloud infrastructure for deployment, database hosting, file storage, and secrets management. The project is a solo portfolio project, so cost, simplicity, and native integration between services are key factors. The backend runs on FastAPI (Python), the frontend is a React SPA, and the database is PostgreSQL.

---

## Decision

We use **Google Cloud Platform (GCP)** with the following services:
- **Cloud Run** — backend deployment (serverless containers, pay-per-use)
- **Cloud SQL** — managed PostgreSQL (automated backups, no server management)
- **Cloud Storage** — file uploads (task attachments)
- **Secret Manager** — environment variable and secrets management
- **Firebase Hosting** — frontend SPA deployment (free tier, CDN included)
- **Cloud Logging** — structured application logs
- **Cloud Build** — CI/CD pipeline integration

GCP Project ID: `stepup-494114`
Region: `europe-west4` (Netherlands — GDPR alignment)

---

## Alternatives Considered

**AWS**
AWS has the largest ecosystem and most documentation. However, for a solo project the number of services and IAM complexity adds overhead. GCP's Cloud Run and Cloud SQL are simpler to set up for this specific stack compared to ECS + RDS.

**Heroku**
Heroku is developer-friendly and fast to set up. However, it was removed from the free tier in 2022. For a portfolio project, GCP provides more impressive and recognizable infrastructure on a CV.

**TransIP VPS (used in EAP)**
TransIP was used in a previous project (EAP). It requires manual server management (nginx, systemd, SSL certificates). GCP managed services eliminate this operational overhead entirely.

---

## Consequences

**Gained:**
- Cloud Run auto-scales to zero — no cost when not in use
- Cloud SQL provides automated daily backups out of the box
- Secret Manager eliminates `.env` files from the repository entirely
- All services are in the same GCP project — IAM and networking are simpler
- `europe-west4` (Netherlands) region aligns with GDPR requirements
- Firebase Hosting provides a free CDN for the React SPA

**Trade-offs:**
- GCP has a learning curve compared to simpler platforms like Heroku
- Cloud SQL has a minimum cost even when idle (unlike serverless DB options)
- Setting up GCP early (Sprint 1) turned out to be a YAGNI violation — infrastructure was ready before there was anything to deploy. Next project: set up cloud infra when the first deployable feature is complete.

**Key configuration decisions:**
- Port 5433 used for local PostgreSQL (port 5432 was occupied by EAP project)
- asyncpg driver for FastAPI (async), psycopg2 driver for Alembic (sync) — two drivers required