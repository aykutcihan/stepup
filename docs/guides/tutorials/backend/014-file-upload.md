# File Upload with FastAPI

How to accept file uploads in a FastAPI endpoint, validate them, save them to disk, and serve them as static files.

---

## The Moving Parts

A file upload endpoint has three concerns:

1. **Receiving** — FastAPI's `UploadFile` reads the request body as a stream
2. **Validating** — content type and size must be checked before saving
3. **Serving** — saved files need a URL the client can fetch

---

## Receiving the File

Use `UploadFile` and `File` from `fastapi`:

```python
from fastapi import APIRouter, Depends, File, UploadFile

@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    ...
```

`File(...)` makes the parameter required. The client must send `multipart/form-data`, not JSON.

`UploadFile` exposes:
- `file.content_type` — MIME type reported by the client (`"image/jpeg"`, etc.)
- `await file.read()` — reads the full content into memory as `bytes`
- `file.filename` — original filename from the client (do not trust this for saving)

---

## Validating Content Type and Size

**Never trust `content_type` alone** — a client can send any string there. Validate it, but treat it as a hint, not a guarantee.

```python
_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
_MAX_BYTES = 5 * 1024 * 1024  # 5MB

if file.content_type not in _ALLOWED_TYPES:
    raise HTTPException(status_code=400, detail="Only JPEG, PNG and WebP images are allowed.")

content = await file.read()

if len(content) > _MAX_BYTES:
    raise HTTPException(status_code=400, detail="Image must be under 5MB.")
```

Read the content **after** the type check so you avoid reading a large file unnecessarily.

For stronger validation, consider checking the file's magic bytes (the first few bytes that identify the format). See the existing magic-bytes validation for reference.

---

## Saving to Disk

Use `pathlib.Path` — it is cleaner than `os.path` and works on all platforms:

```python
from pathlib import Path

_UPLOAD_DIR = Path("uploads/avatars")
_EXT_MAP = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}

_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ext = _EXT_MAP[file.content_type]
filename = f"{current_user.id}.{ext}"
(_UPLOAD_DIR / filename).write_bytes(content)
```

**Filename strategy:** use the user's UUID as the filename, not `file.filename`. This prevents:
- Path traversal attacks (`../../etc/passwd`)
- Collisions between users
- Special characters that break filesystems

Using the user ID also means uploading a new photo overwrites the previous one automatically.

---

## Storing the Path in the Database

Store the URL path (not the filesystem path) so the client can fetch it directly:

```python
current_user.avatar_url = f"/static/avatars/{filename}"
db.add(current_user)
await db.commit()
await db.refresh(current_user)
```

`/static/avatars/filename.jpg` is the path FastAPI will serve via `StaticFiles` (see below). The client prepends the backend base URL to get the full URL.

---

## Serving Uploaded Files

Mount a `StaticFiles` handler in `main.py` so FastAPI serves the `uploads/` directory:

```python
import os
from fastapi.staticfiles import StaticFiles

os.makedirs("uploads/avatars", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")
```

`app.mount` must be called **before** `app.include_router` — router routes take precedence and would shadow the static mount if registered first.

After this, a file saved at `uploads/avatars/abc123.jpg` is accessible at:

```
GET http://localhost:8000/static/avatars/abc123.jpg
```

---

## Full Endpoint Example

```python
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
_EXT_MAP = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
_UPLOAD_DIR = Path("uploads/avatars")
_MAX_BYTES = 5 * 1024 * 1024

router = APIRouter()

@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG and WebP images are allowed.")

    content = await file.read()
    if len(content) > _MAX_BYTES:
        raise HTTPException(status_code=400, detail="Image must be under 5MB.")

    _UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ext = _EXT_MAP[file.content_type]
    filename = f"{current_user.id}.{ext}"
    (_UPLOAD_DIR / filename).write_bytes(content)

    current_user.avatar_url = f"/static/avatars/{filename}"
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return UserResponse.model_validate(current_user)
```

---

## Displaying on the Frontend

The stored `avatar_url` is a relative path like `/static/avatars/abc123.jpg`. The frontend must prepend the backend base URL:

```typescript
const API_URL = import.meta.env.VITE_API_URL ?? ''

const avatarSrc = user.avatar_url ? `${API_URL}${user.avatar_url}` : null
```

Then use it in JSX:

```tsx
{avatarSrc ? (
  <img src={avatarSrc} alt="Avatar" className="w-full h-full object-cover" />
) : (
  <span>{initials}</span>
)}
```

---

## Production Note

Local disk storage (`uploads/`) works for development but does not survive container restarts on Cloud Run — the filesystem is ephemeral. Before deploying to production, replace disk writes with GCP Cloud Storage uploads and store the full public GCS URL in `avatar_url` instead. See ADR-002 for the GCP stack decision.
