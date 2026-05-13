# Soft Delete — Frontend Perspective

Backend soft delete doc: `docs/guides/tutorials/backend/010-soft-delete.md`

This document covers how the frontend handles soft-deleted entities.

---

## What the Backend Sends

Soft-deleted entities are never removed from API responses. Instead, the response includes a boolean flag:

```ts
// UserResponse
is_active: boolean

// DepartmentResponse
is_active: boolean
```

The frontend receives all records — active and inactive — and decides what to show based on `is_active`.

---

## Rule: Never Filter Inactive Records from Lists

Admin views show everything. `is_active` is displayed as a status badge — the HR Admin sees both active and inactive records and can act on them.

```tsx
// ✅ Show all, display status
{departments.map((d) => (
  <tr key={d.id}>
    <td>{d.name}</td>
    <td>{d.is_active ? 'Active' : 'Inactive'}</td>
    <td>
      {d.is_active
        ? <button onClick={() => handleDeactivate(d.id)}>Deactivate</button>
        : <button onClick={() => handleReactivate(d.id)}>Reactivate</button>
      }
    </td>
  </tr>
))}
```

---

## Rule: Filter Inactive Records from Dropdowns

When a user selects a department to assign to another user, inactive departments must not appear. Showing a deactivated department as a selectable option would let the user assign someone to a department that no longer exists operationally.

```ts
// In the hook — split into two lists
const activeDepartments = departments.filter((d) => d.is_active)

// In the page — admin list uses departments (all)
//               assignment dropdown uses activeDepartments (active only)
{activeDepartments.map((d) => (
  <option key={d.id} value={d.id}>{d.name}</option>
))}
```

---

## Deactivate / Reactivate Flow

The frontend calls a dedicated endpoint for each state transition — never sends `is_active` directly as a field in a PATCH body.

```ts
// ✅ Dedicated endpoints
deactivateDepartment(id)   // PATCH /departments/{id}/deactivate
reactivateDepartment(id)   // PATCH /departments/{id}/reactivate

// ❌ Not this
updateDepartment(id, { is_active: false })
```

**Why?** State transitions have business rules on the backend (e.g. cannot deactivate a department with active users). A dedicated endpoint makes the intent explicit and lets the backend enforce the rule cleanly.

---

## Error Handling for Business Rule Violations

When the backend rejects a deactivation (e.g. department has active users), it returns a structured error:

```json
{ "error_code": "DEPARTMENT_HAS_ACTIVE_USERS" }
```

The frontend maps this to a human-readable message via `errorMessages.ts` and displays it inline:

```ts
// constants/errorMessages.ts
DEPARTMENT_HAS_ACTIVE_USERS: 'Cannot deactivate a department with active users.'
```

```ts
// In the hook
async function handleDeactivate(id: string) {
  try {
    const updated = await deactivateDepartment(id)
    setDepartments((prev) => prev.map((d) => (d.id === updated.id ? updated : d)))
    setPageError('')
  } catch (err: unknown) {
    const code = (err as { response?: { data?: { error_code?: string } } }).response?.data?.error_code
    setPageError(ERROR_MESSAGES[code ?? ''] ?? 'Something went wrong.')
  }
}
```

The page renders `pageError` inline above the table — no modal, no toast, no redirect.

---

## Summary

| Situation | Behaviour |
|-----------|-----------|
| Admin list | Show all records (active + inactive) |
| Assignment dropdown | Show active records only |
| Deactivate action | Call dedicated endpoint, catch business rule errors |
| Reactivate action | Call dedicated endpoint |
| Backend rejects | Show inline error message from `errorMessages.ts` |
