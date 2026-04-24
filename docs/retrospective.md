# Retrospective

## Sprint 1 — Foundation

### What Went Well
- Monorepo, Docker, and database schema set up cleanly with no major rework
- Technical decisions documented in ADR before writing code
- Port conflict (5432 → 5433) caught and resolved early in local environment
- Alembic + asyncpg/psycopg2 dual-driver pattern understood and applied correctly
- GitHub issue templates created for all subtask types (BE, BE TEST, FE, FE TEST, DOC, DEVOPS, E2E)
- Full US list (34 US + 10 Epics + 9 E2E) defined and added to project board

### What Needs Improvement
- GCP and CI set up before there was anything to deploy or test — violated YAGNI
- Seed data and Department CRUD added to Sprint 1 without dependencies being ready
- Early infrastructure setup created unexpected blockers (asyncpg build failure, psycopg2 missing) that slowed down actual feature work

### Next Steps
- Move US-005 (Department CRUD) and US-011 (Seed data) out of Sprint 1 — already done
- GCP and CI: treat as "done but early" — noted in ADR-002
- Sprint 2: focus only on Auth (US-001 through US-007) before touching anything else
- Rule for next sprint: before adding a US, ask "does anything break today without this?"