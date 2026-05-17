from datetime import timedelta

import google.auth
import google.auth.transport.requests
from google.cloud import storage

from app.core.config import settings
from app.errors import ValidationError, messages

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

FILE_SIGNATURES: dict[str, tuple[bytes, ...]] = {
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "application/pdf": (b"%PDF",),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
        b"PK\x03\x04",
    ),
}


class StorageService:

    def __init__(self) -> None:
        self._client: storage.Client | None = None

    def _get_bucket(self) -> storage.Bucket:
        if self._client is None:
            self._client = storage.Client()
        return self._client.bucket(settings.GCS_BUCKET_NAME)

    def validate_file_signature(self, content: bytes, content_type: str) -> None:
        allowed_signatures = FILE_SIGNATURES.get(content_type)
        if not allowed_signatures:
            raise ValidationError(*messages.INVALID_FILE_TYPE)
        if not any(content.startswith(sig) for sig in allowed_signatures):
            raise ValidationError(*messages.INVALID_FILE_TYPE)

    def upload(self, content: bytes, object_name: str, content_type: str) -> str:
        blob = self._get_bucket().blob(object_name)
        blob.upload_from_string(content, content_type=content_type)
        return object_name

    def delete(self, object_name: str) -> None:
        blob = self._get_bucket().blob(object_name)
        if blob.exists():
            blob.delete()

    def signed_url(self, object_name: str, expiration_minutes: int = 60) -> str:
        credentials, _ = google.auth.default()
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)

        blob = self._get_bucket().blob(object_name)

        extra: dict = {}
        email = getattr(credentials, "service_account_email", None)
        token = getattr(credentials, "token", None)
        if email and email != "default" and token:
            extra["service_account_email"] = email
            extra["access_token"] = token

        return blob.generate_signed_url(
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
            version="v4",
            **extra,
        )
