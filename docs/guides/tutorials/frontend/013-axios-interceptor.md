# Axios Interceptor

## What It Does

An interceptor is a function that runs automatically before every request or after every response.
It intercepts the call — you can inspect it, modify it, retry it, or redirect.

This project uses a **response interceptor** to handle expired access tokens transparently.

---

## The Problem Without an Interceptor

Access tokens expire after 15 minutes. Without an interceptor, every component that makes an API call would need to handle 401 errors manually:

```
Component → API call → 401 → try refresh → retry → redirect to login if failed
```

That is the same logic repeated in every service function. An interceptor puts this logic in one place — components never see the 401.

---

## How It Works

```
Component calls API
→ Access token expired → server returns 401
→ Interceptor catches 401 before the component sees it
→ Interceptor calls POST /auth/refresh
    → Refresh success  → retry original request → component gets its data
    → Refresh fails    → redirect to /login
```

---

## Implementation

Added to `apiClient.ts`:

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        await apiClient.post(API.AUTH.REFRESH)
        return apiClient(original)
      } catch {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)
```

**`_retry` flag:** Prevents infinite loops. If the retried request also returns 401, the interceptor does not trigger again — it falls through to `Promise.reject`.

**`window.location.href`:** Used instead of `navigate()` because the interceptor lives outside React — React Router's `useNavigate` can only be called inside a component.

---

## Two Interceptor Types

```typescript
apiClient.interceptors.request.use(...)   // runs before every request
apiClient.interceptors.response.use(...)  // runs after every response
```

This project only uses the response interceptor. Request interceptors are typically used to attach headers (e.g. auth tokens in Bearer token setups) — not needed here because tokens are HttpOnly cookies sent automatically by the browser.
