# Frontend Package Reference

Every dependency in `package.json` — what it does and why it is there.

---

## Dependencies (Runtime)

These are included in the production build.

### `react` and `react-dom`

The core React library.

- `react` → the component model, hooks, JSX runtime
- `react-dom` → renders React components to the browser DOM

Both are always installed together. `react-dom` is the browser-specific renderer — React itself is platform-agnostic (can also render to native mobile via React Native).

### `react-router-dom`

Client-side routing. Enables navigation between pages without full page reloads.

```typescript
<Routes>
  <Route path="/login" element={<LoginPage />} />
  <Route path="/hr/dashboard" element={<HRDashboard />} />
</Routes>
```

Used for all page routing, protected routes, and redirects. See `product-vision.md` for the full route structure.

### `@tanstack/react-query`

Server state management. Handles API calls, caching, loading states, and error states.

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['invitations'],
  queryFn: () => api.getInvitations(),
})
```

Without React Query, every component that fetches data needs to manually manage loading, error, and data state. React Query handles this automatically, with built-in cache invalidation and background refetching.

See ADR-003 for the decision to use React Query over other options.

### `zustand`

Client state management. Stores UI state that does not come from the server — logged-in user info, role, active modals.

```typescript
const useAuthStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))
```

Lightweight alternative to Redux. Used for auth state only — everything else goes through React Query.

See ADR-003 for the decision to use Zustand.

### `axios`

HTTP client for API calls. Used with interceptors to handle token refresh automatically.

```typescript
const api = axios.create({ baseURL: '/api/v1', withCredentials: true })
```

`withCredentials: true` ensures cookies (HttpOnly auth tokens) are sent with every request.

The interceptor catches 401 responses, calls `/auth/refresh`, and retries the original request — transparent token refresh without the user noticing.

### `react-hook-form`

Form state management. Handles input values, validation, and submission without unnecessary re-renders.

```typescript
const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
  resolver: zodResolver(loginSchema),
})
```

Alternative to controlled inputs (`useState` for every field). React Hook Form uses uncontrolled inputs under the hood — faster, especially for large forms.

### `zod`

Schema validation library. Defines the shape and constraints of form data.

```typescript
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})
```

Used with `react-hook-form` via `zodResolver`. The schema validates on submit and provides typed form data — `handleSubmit` receives `{ email: string, password: string }`, not untyped form values.

### `date-fns`

Date utility library. Formats dates for display.

```typescript
formatDistanceToNow(new Date(task.deadline))  // "3 days from now"
format(new Date(invitation.expires_at), 'MMM d, yyyy')  // "May 12, 2026"
format(new Date(invitation.expires_at), 'dd/MM/yyyy')   // "13/05/2026"
```

**Why not `new Date().toLocaleDateString()`?**

Browser's built-in date formatting varies by locale and browser. `date-fns` gives consistent output everywhere.

**Import only what you need:**
```typescript
import { format } from 'date-fns'        // only format
import { formatDistanceToNow } from 'date-fns'  // only this one
```

Tree-shakeable — unused functions are not included in the bundle. Lighter than `moment.js` which ships everything regardless.

---

## DevDependencies (Build and Development Only)

These are not included in the production bundle.

### `vite` and `@vitejs/plugin-react`

The build tool and React plugin. See `001-vite.md`.

### `typescript`

The TypeScript compiler. Only used for type checking (`tsc --noEmit`) — Vite handles the actual transpilation via esbuild.

### `vitest` and `@vitest/coverage-v8`

Test runner and coverage reporter. See `003-vitest.md`.

`@vitest/coverage-v8` uses Node's built-in V8 coverage engine — faster than Istanbul (which `@vitest/coverage-istanbul` uses).

### `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`

Test utilities for React components.

- `@testing-library/react` → renders components, queries the DOM (`getByRole`, `getByText`, etc.)
- `@testing-library/user-event` → simulates user interactions (`userEvent.click`, `userEvent.type`)
- `@testing-library/jest-dom` → custom matchers (`toBeInTheDocument`, `toHaveValue`)

The Testing Library philosophy: test components the way a user would use them — by labels, roles, and text — not by implementation details (class names, internal state).

### `@types/react`, `@types/react-dom`, `@types/node`

TypeScript type definitions.

- `@types/react` → types for React APIs, JSX elements, hooks
- `@types/react-dom` → types for `createRoot`, `render`
- `@types/node` → types for Node.js globals used in config files (`__dirname`, `path`, `process`)

### `tailwindcss`, `postcss`, `autoprefixer`

CSS toolchain. See `004-tailwind.md`.

### `eslint`, `@eslint/js`, `typescript-eslint`, `eslint-plugin-react-hooks`

Linting toolchain. See `005-eslint.md`.

### `jsdom`

Browser environment simulation for Node.js. Used by Vitest as the test environment. See `003-vitest.md`.
