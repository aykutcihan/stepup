# GCP Setup

## Why GCP?

Your application needs 3 things to run in production:

```
1. A place to run          → Cloud Run
2. A place to store data   → Cloud SQL
3. A place to store secrets → Secret Manager
```

GCP provides all 3. We chose GCP because:
- Free trial with €260 credits
- Cloud Run scales automatically — pay only for what you use
- All services work together natively
- Strong presence in Netherlands (europe-west4 region)

---

## Local vs Production

```
Local (your computer):
  Database  → PostgreSQL container via docker-compose
  Secrets   → .env file (never committed to GitHub)

Production (GCP):
  Database  → Cloud SQL
  Secrets   → Secret Manager
```

Same application code — different infrastructure depending on environment.

---

## Step 1: Enable APIs

GCP services are disabled by default — for security.
You must enable each service before using it.

**APIs we enabled:**

| API | Why |
|---|---|
| Cloud Run Admin API | Deploy and run backend container |
| Cloud SQL Admin API | Manage PostgreSQL database |
| Secret Manager API | Store sensitive values securely |
| Cloud Build API | Automated builds in CI/CD pipeline |

**How to enable:**
```
GCP Console → APIs & Services → Enable APIs and Services
→ Search for API name → Click Enable
```

---

## Step 2: Cloud SQL

Cloud SQL = PostgreSQL running on GCP's servers.

**Difference from local PostgreSQL:**

```
Local PostgreSQL  → runs on your computer only
                    stops when you close your laptop
                    only you can access it

Cloud SQL         → runs on GCP servers 24/7
                    accessible from anywhere on the internet
                    GCP handles backups and maintenance
```

**What we created:**

```
Instance:  stepup-db
Engine:    PostgreSQL 18
Region:    europe-west4 (Netherlands) ← close to our users
Public IP: 34.32.215.164
Port:      5432

Database:  stepup_db    ← where our data lives
User:      stepup_user  ← application connects with this user
```

**Why Netherlands region?**
- Lower latency for Dutch users
- GDPR compliance — data stays in EU
- Closer to our deployment region

**How to navigate:**
```
GCP Console → hamburger menu (☰) → SQL → Create Instance
```

---

## Step 3: Secret Manager

### The Problem

Your application needs sensitive values to run:
```
DATABASE_URL    → database connection string + password
JWT_SECRET_KEY  → used to sign and verify JWT tokens
SENDGRID_API_KEY → used to send emails
```

Where do you put these?

| Option | Problem |
|---|---|
| In the code | Visible to everyone who reads your code |
| In .env file | Can accidentally be committed to GitHub |
| Secret Manager | Encrypted, access-controlled, logged |

### What is Secret Manager?

Secret Manager = a secure vault for sensitive values.

```
You store:  DATABASE_URL = postgresql://stepup_user:xxx@34.32.215.164/stepup_db
GCP stores: encrypted version, no one can read it directly
App reads:  GCP gives the value to the app at runtime
```

### What we stored:

| Secret | Purpose |
|---|---|
| `DATABASE_URL` | Full connection string to Cloud SQL |
| `JWT_SECRET_KEY` | Signs and verifies JWT access tokens |
| `SENDGRID_API_KEY` | Authenticates with SendGrid email service |
| `SENDGRID_FROM_EMAIL` | Verified sender email address for SendGrid |

**How to navigate:**
```
GCP Console → hamburger menu (☰) → Security → Secret Manager
→ Create Secret → Name + Value → Create
```

### Local vs Production secrets

```
Local development:
  → .env file (added to .gitignore, never goes to GitHub)
  → docker-compose reads from .env

Production (GCP Cloud Run):
  → No .env file
  → App reads secrets from Secret Manager at startup
  → Uses Service Account for authentication (automatic in Cloud Run)
```

### What is a Service Account?

You log into GCP with email + password — you are a human.
The backend application also needs to access GCP — but it is not a human.

```
You          → email + password → GCP access
Backend app  → Service Account  → GCP access
```

Service Account = the application's identity card.

In Cloud Run, this is automatic — the app uses the project's
default Service Account. No extra configuration needed.

---

## GCS Signed URLs on Cloud Run

When the backend generates download links for file attachments, it uses GCS signed URLs. Signed URL generation requires signing credentials.

**Local development:** ADC points to a service account JSON key file — private key available, signing works automatically.

**Cloud Run:** Credentials come from the GCP metadata server as a token only — no private key. Calling `blob.generate_signed_url()` without explicit credentials raises `AttributeError`.

**Fix — IAM-based signing:**

Pass `service_account_email` and `access_token` to `generate_signed_url`. The GCS library delegates signing to the IAM API:

```python
credentials, _ = google.auth.default()
credentials.refresh(google.auth.transport.requests.Request())

blob.generate_signed_url(
    expiration=timedelta(minutes=60),
    method="GET",
    version="v4",
    service_account_email=credentials.service_account_email,
    access_token=credentials.token,
)
```

**Required IAM role** — the Cloud Run service account must have:

```bash
gcloud projects add-iam-policy-binding stepup-494114 \
  --member="serviceAccount:943378472223-compute@developer.gserviceaccount.com" \
  --role="roles/iam.serviceAccountTokenCreator"
```

Without this role, the IAM signing call returns 403.

**Cloud Run service account:** `943378472223-compute@developer.gserviceaccount.com`

---

## Step 4: Cloud Run (coming later)

Cloud Run = runs our backend Docker container on GCP.

We will set this up together with the CI/CD pipeline (GitHub Actions).
When we push code to `main`, GitHub Actions will:
1. Build the Docker image
2. Push it to GCP
3. Deploy it to Cloud Run automatically

---

## Summary

```
What we did in GCP so far:

✅ Enabled 4 APIs
✅ Created Cloud SQL instance (stepup-db)
✅ Created database (stepup_db)
✅ Created database user (stepup_user)
✅ Stored 3 secrets in Secret Manager

Still to do:
⏳ Cloud Run setup (with CI/CD)
⏳ Firebase Hosting (for frontend)
```

---

## Key Information to Remember

```
Project ID:       stepup-494114
Project Number:   943378472223
Region:           europe-west4
SQL Instance:     stepup-494114:europe-west4:stepup-db
Public IP:        34.32.215.164
Database:         stepup_db
DB User:          stepup_user
```

> Never commit these values to GitHub.
> Store them in Secret Manager or local .env file only.