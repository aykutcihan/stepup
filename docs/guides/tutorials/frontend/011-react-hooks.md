# React Hooks

## What is a Hook?

A hook is a function that starts with `use`. Hooks let you use React features inside function components — state, side effects, form management, routing.

You cannot call hooks inside conditions, loops, or nested functions. Always call them at the top level of a component.

---

## useState

### The Problem With Regular Variables

```typescript
let email = ''
email = 'ali@test.com'  // value changed — but the screen does not update
```

React does not know the variable changed. The component does not re-render.

### useState — Change a Value and Update the Screen

```typescript
const [email, setEmail] = useState('')
setEmail('ali@test.com')  // value changed AND screen updates
```

`useState` returns two things:
- `email` → current value
- `setEmail` → function that changes the value and triggers a re-render

```typescript
const [value, setValue] = useState(initialValue)
//     ↑ read    ↑ write   ↑ starting value
```

**When to use:** Any value that, when changed, should update what the user sees on screen.

In `RegisterPage`:
```typescript
const [email, setEmail] = useState('')       // pre-filled email from BE
const [pageError, setPageError] = useState('') // error message to display
```

---

## useEffect

### The Problem

React renders components many times. If you call an API directly in the component body, it fires on every render — potentially dozens of requests.

```typescript
// ❌ Wrong — runs on every render
export default function RegisterPage() {
  validateInvitation(token)  // called every time React re-renders this component
  ...
}
```

### useEffect — Run Code After Render

```typescript
useEffect(() => {
  // runs after the component renders
  validateInvitation(token)
}, [token])
```

The second argument `[token]` is the **dependency array** — "run this effect when `token` changes."

| Dependency array | When it runs |
|---|---|
| `[token]` | On first render and whenever `token` changes |
| `[]` | Only on first render (once) |
| nothing | On every render — usually wrong |

In `RegisterPage`, `token` comes from the URL and never changes — so the effect runs exactly once when the page loads.

### useEffect Cannot Be async

```typescript
// ❌ Not allowed
useEffect(async () => {
  await validateInvitation(token)
}, [token])
```

React does not support async useEffect directly. Use `.then/.catch` instead:

```typescript
// ✅ Correct
useEffect(() => {
  validateInvitation(token)
    .then((data) => setEmail(data.email))
    .catch((err) => setPageError(getErrorMessage(err)))
}, [token])
```

---

## .then/.catch vs async/await

Both handle Promises — asynchronous operations that will complete in the future.

### .then/.catch — Promise chaining

```typescript
validateInvitation(token)
  .then((data) => setEmail(data.email))   // runs on success
  .catch((err) => setPageError(...))      // runs on failure
```

### async/await + try/catch

```typescript
const onSubmit = async (data: FormData) => {
  try {
    await register({ token, ...data })   // wait for result
    navigate(ROUTES.LOGIN)               // runs on success
  } catch (err) {
    setPageError(getErrorMessage(err))   // runs on failure
  }
}
```

**Which to use:**
- Inside `useEffect` → `.then/.catch` (because useEffect cannot be async)
- Inside `async` functions → `try/catch` with `await` (cleaner to read)

Both are correct. The choice is about readability and context.

---

## useForm + Zod

### The Problem With useState for Forms

```typescript
// ❌ A separate state for every field
const [firstName, setFirstName] = useState('')
const [lastName, setLastName] = useState('')
const [password, setPassword] = useState('')
// Each keystroke triggers a re-render for that field
```

### useForm — Manages All Fields at Once

React Hook Form uses uncontrolled inputs under the hood — the DOM tracks values, not React state. No re-render on every keystroke.

```typescript
const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
})
```

Three things come out of `useForm`:

**`register`** — connects an input to the form:
```tsx
<input {...register('first_name')} placeholder="First name" />
```
`{...register('first_name')}` spreads `{ name, onChange, onBlur, ref }` onto the input. The form now tracks this field.

**`handleSubmit`** — intercepts form submission:
```tsx
<form onSubmit={handleSubmit(onSubmit)}>
```
Runs Zod validation first. If all fields pass → calls `onSubmit` with the form data. If any field fails → populates `errors`, does not call `onSubmit`.

**`errors`** — validation error messages:
```tsx
{errors.first_name && <p>{errors.first_name.message}</p>}
```
If `first_name` failed validation, `errors.first_name.message` contains the message defined in the Zod schema.

### Zod Schema

Defines the validation rules:

```typescript
const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})
```

`resolver: zodResolver(schema)` connects the schema to `useForm` — React Hook Form uses Zod to validate on submit.

### z.infer — Automatic TypeScript Type

```typescript
type FormData = z.infer<typeof schema>
```

Instead of writing the TypeScript type manually, Zod generates it from the schema. `FormData` automatically becomes:

```typescript
{
  first_name: string
  last_name: string
  password: string
}
```

When the schema changes, the TypeScript type updates automatically — no manual sync needed.

---

## Dropdown Fields — z.enum and select

### z.enum — Validate Against a Fixed Set of Values

Text inputs use `z.string()`. Dropdowns have a fixed set of allowed values — use `z.enum()`:

```typescript
const schema = z.object({
  role: z.enum(['employee', 'manager', 'hr_admin']),
})
```

If any value other than these three is submitted, Zod rejects it. Mirrors the BE's `UserRole` enum exactly.

### select + register

A `<select>` element connects to React Hook Form the same way as `<input>` — using `register`:

```tsx
<select {...register('role')}>
  <option value="employee">Employee</option>
  <option value="manager">Manager</option>
  <option value="hr_admin">HR Admin</option>
</select>
{errors.role && <p>{errors.role.message}</p>}
```

`{...register('role')}` spreads `name`, `onChange`, `onBlur`, `ref` onto the `<select>`. React Hook Form tracks the selected value automatically. The `value` of each `<option>` must match the enum values in the Zod schema.

---

## useNavigate and useSearchParams

### useNavigate — Go to Another Page in Code

```typescript
const navigate = useNavigate()
navigate(ROUTES.LOGIN)  // goes to /login
```

Used after a successful action — register complete, login complete.

### useSearchParams — Read the URL Query String

```typescript
const [searchParams] = useSearchParams()
const token = searchParams.get('token') ?? ''
```

Reads `?token=abc123` from the URL. `searchParams.get('token')` returns `"abc123"` or `null` if not present. `?? ''` provides an empty string fallback if null.
