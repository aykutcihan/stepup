# Frontend Test Conventions

This guide covers how we structure, name, and write frontend tests in this project.

---

## Directory Structure

Test files live next to the component they test (co-located):

| Source file | Test file |
|-------------|-----------|
| `src/features/auth/pages/LoginPage.tsx` | `src/features/auth/pages/LoginPage.test.tsx` |
| `src/features/invitation/pages/RegisterPage.tsx` | `src/features/invitation/pages/RegisterPage.test.tsx` |
| `src/components/RequireRole.tsx` | `src/components/RequireRole.test.tsx` |

`tests/` directory keeps only `setup.ts` and `e2e/` (Playwright).

---

## Grouping and Naming

Flat structure — one `describe` per component, `it` describes the behavior:

```ts
describe('LoginPage', () => {
  it('renders email and password inputs', ...)
  it('shows validation errors on empty submit', ...)
  it('navigates to HR dashboard on successful login', ...)
})
```

`it` names start with a verb: `renders`, `shows`, `navigates`, `calls`, `displays`.

---

## Mock Naming

**Service functions:** `mock` + module name + function name (camelCase)

```ts
const mockAuthServiceLogin = vi.fn()
const mockAuthServiceGetMe = vi.fn()
const mockInvitationServiceCreate = vi.fn()
```

**Mock objects:** `mock` + type name (camelCase)

```ts
const mockUser = { id: '1', email: 'test@test.com', role: 'hr_admin' }
const mockInvitation = { id: '2', email: 'new@test.com', role: 'employee' }
```
