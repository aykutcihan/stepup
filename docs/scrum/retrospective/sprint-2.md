# Sprint 2 — Retrospective

*To be filled at the end of Sprint 2.*

### What Went Well

### What Needs Improvement
- `GET /auth/me` endpoint was missing from the original US-002 BE scope — login endpoint intentionally returns no user data, but there was no endpoint to fetch current user info after login. Discovered during FE implementation. Rule: when designing an auth flow, explicitly define how the FE gets user info post-login.
- `GET /users` endpoint was missing from the original US-003 BE scope — needed by FE to display the user list for deactivation. Discovered during FE implementation. Rule: when a FE feature requires listing resources, verify the corresponding BE list endpoint exists before starting FE work.
- Frontend test directory was created inside `src/test/` instead of `tests/` at the project root level. Discovered when writing the first component tests. Fixed by moving `setup.ts` and updating `vitest.config.ts`. Later revised: unit test files are co-located next to their component (e.g. `LoginPage.test.tsx` next to `LoginPage.tsx`). `tests/` keeps only `setup.ts` and `e2e/`. See `009-fe-test-conventions.md`.
- Board became too large (80+ items in one view) — added `subtask` label and sprint-based views filtered by `-label:subtask`
- Feature branches had no remote tracking — branches stayed local only. Rule: always push branch to remote immediately after first commit (`git push origin branch-name`)
- Feature branches were not merged to develop — discovered via `git log --oneline` and `ls docs/`. Rule: at the end of each sprint, verify develop is up to date with `git log --oneline`
- Commit messages were inconsistent — no standard existed. Rule: all commits must follow the convention in `02-commit-convention.md`

### Decisions Made Before Writing FE Tests

- **Co-located test files** — unit test files live next to the component they test, not in a mirrored `tests/` directory. Easier to find and harder to forget to delete.
- **Flat describe/it structure** — one `describe` per component, `it` names start with a verb (`renders`, `shows`, `navigates`, `calls`). No nested `describe` blocks — test count is too small to justify nesting.
- **Mock naming** — service function mocks: `mockAuthServiceLogin` (camelCase, module + function name). Mock objects: `mockUser`, `mockInvitation`.
- **Separate BE/FE test convention docs** — `008-be-test-conventions.md` and `009-fe-test-conventions.md` instead of a single shared file.

### Next Steps
