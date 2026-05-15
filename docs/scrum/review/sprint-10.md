# Sprint 10 — Review

## Sprint Goal
Employees can upload documents and add comments to onboarding tasks. Files are stored securely in GCP Cloud Storage. Managers can see uploaded files when reviewing tasks.

## Sprint Goal Achieved?
Yes — US-014b fully delivered.

## Completed User Stories

| US | Title | Status | Notes |
|----|-------|--------|-------|
| US-014b | File Upload & Comments | Done | GCS bucket, 3 endpoints, signed URLs, expandable task panel, 6 unit tests |

## Incomplete / Deferred User Stories

| US | Title | Reason | Moved to |
|----|-------|--------|----------|
| US-021 | Technical Quality & Polish | Natural final sprint | Sprint 11 |

## Metrics
- USs planned: 1
- USs completed: 1
- PRs merged: 1 (#194)

## Key Decisions Made This Sprint

### GCS bucket created via gcloud — not Console
Bucket `stepup-494114-attachments` was created programmatically using `gcloud storage buckets create`. Compute service account granted `Storage Object Admin` directly on the bucket (not project-wide). `GCS_BUCKET_NAME` stored in Secret Manager. Service account key created for local dev, added to `.gitignore` and mounted as a read-only Docker volume.

### Files stored by object name, signed URL generated per request
`TaskAttachment.object_name` stores the GCS path (`tasks/{task_id}/{uuid}_{filename}`). The `file_url` / `download_url` in the API response is a v4 signed URL generated fresh on each request (1-hour expiry). This means no stale URLs in the DB — each API call returns a valid link.

### StorageService lazily initializes GCS client
`StorageService._client` is `None` on import and instantiated on first call. This prevents the GCS client from being created at module load time (which would fail in test environments without credentials), and lets unit tests patch `storage.Client` easily.

### Attachment delete guarded by two rules: ownership + approval state
- Only the uploader can delete their own attachment (`uploaded_by == current_user.id` check)
- Once the task is `APPROVED`, attachments are locked — prevents post-approval evidence tampering
- Both checks happen before GCS delete call to avoid partial state

### Plan repository extended to selectinload attachments + comments
All plan queries (`get_by_id`, `get_active_by_user`, `get_all_by_manager`) now chain `selectinload(OnboardingPlan.tasks).options(selectinload(OnboardingPlanTask.attachments), selectinload(OnboardingPlanTask.comments))`. This is the correct async SQLAlchemy pattern for nested eager loading — avoids N+1 and lazy-load errors in async context.

### FE uses expandable task rows — not a separate page
Clicking a task title expands an inline panel (attachments + upload input + comment form). No new route needed. `useEmployeePlanPage` hook manages optimistic state updates for all three operations (upload, delete, comment) without refetching the full plan.

## Allowed File Types

| MIME type | Extension |
|-----------|-----------|
| `application/pdf` | .pdf |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | .docx |
| `image/png` | .png |
| `image/jpeg` | .jpg / .jpeg |

Max size: 10 MB

## US-198 — Dark / Light / System Theme ✅ Done

Delivered on `feature/us-198-theme-support` branching from `develop`.

### What was built

- **Three-way theme toggle** (Light / Dark / System) in the hamburger menu on all layouts
- Theme collapses under a "Theme ▼" row — clicking expands the 3 options; selecting one closes the panel
- **`themeStore`** (Zustand, no persist middleware) reads/writes `localStorage` key `stepup-theme` directly in `setTheme` — synchronous apply, no async rehydration race conditions
- **`ThemeProvider`** wraps the app in `main.tsx`; `useEffect([theme])` re-applies the class whenever the store changes; OS media query listener active only in System mode
- **`index.html` inline script** applies the correct class before React mounts to prevent flash of wrong theme; also clears the old zustand-persist JSON format from localStorage if present
- **`tailwind.config.js`**: `darkMode: 'class'` — requires Vite/PostCSS restart to pick up on first use
- All pages fully dark-mode styled: layouts, dashboards, tables, cards, forms, modals, badges

### Root cause of light mode not working (postmortem)

Vite was started before `darkMode: 'class'` was added to `tailwind.config.js`. PostCSS/Tailwind had cached the CSS without class-based dark mode — all `dark:` variants used `@media (prefers-color-scheme: dark)`. Restarting the frontend container forced a CSS rebuild. After restart, removing the `.dark` class from `<html>` immediately switched the page to light mode.

Debug overlay (`ThemeProvider` renders `html.class` + `store theme`) was used to confirm the class was empty but the page was still dark — confirming a CSS/build issue, not a JavaScript issue.

---

## Notes
- `gcs-key.json` is gitignored via `*.json` pattern (with exceptions for `package.json`, `tsconfig*.json`, `turbo.json`)
- `GOOGLE_APPLICATION_CREDENTIALS` env var points to `/app/gcs-key.json` inside the container
- In Cloud Run production, application default credentials are used automatically — no key file needed
- Signed URLs use v4 signing (more secure than v2) and require `google.auth` service account credentials
