from datetime import timedelta

from google.cloud import storage

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class StorageService:

    def __init__(self) -> None:
        self._client: storage.Client | None = None

    def _get_bucket(self) -> storage.Bucket:
        if self._client is None:
            self._client = storage.Client()
        return self._client.bucket(settings.GCS_BUCKET_NAME)

    def upload(self, content: bytes, object_name: str, content_type: str) -> str:
        blob = self._get_bucket().blob(object_name)
        blob.upload_from_string(content, content_type=content_type)
        return object_name

    def delete(self, object_name: str) -> None:
        blob = self._get_bucket().blob(object_name)
        if blob.exists():
            blob.delete()

    def signed_url(self, object_name: str, expiration_minutes: int = 60) -> str:
        blob = self._get_bucket().blob(object_name)
        return blob.generate_signed_url(
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
            version="v4",
        )
