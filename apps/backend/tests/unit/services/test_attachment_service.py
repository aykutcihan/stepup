import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import ValidationError, PermissionError
from app.services.attachment_service import AttachmentService

pytestmark = pytest.mark.asyncio(loop_scope="session")


def _make_task(status=OnboardingPlanTaskStatus.IN_PROGRESS):
    task = MagicMock()
    task.id = uuid.uuid4()
    task.status = status
    task.deleted_at = None
    return task


def _make_attachment(uploaded_by=None, plan_task_id=None):
    att = MagicMock()
    att.id = uuid.uuid4()
    att.uploaded_by = uploaded_by or uuid.uuid4()
    att.plan_task_id = plan_task_id or uuid.uuid4()
    att.object_name = f"tasks/{att.plan_task_id}/test.pdf"
    att.file_name = "test.pdf"
    att.file_type = "application/pdf"
    att.file_size = 1024
    att.created_at = MagicMock()
    return att


def _make_upload_file(content_type="application/pdf", size=1024):
    file = AsyncMock()
    file.content_type = content_type
    file.filename = "test.pdf"
    file.read = AsyncMock(return_value=b"x" * size)
    return file


class TestUploadAttachment:

    async def test_rejects_invalid_mime_type(self):
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()
        task = _make_task()
        file = _make_upload_file(content_type="text/plain")

        with patch("app.services.attachment_service.plan_task_repository") as repo:
            repo.get_by_id = AsyncMock(return_value=task)
            with pytest.raises(ValidationError) as exc:
                await service.upload_attachment(db, task.id, file, user)
        assert exc.value.code == "INVALID_FILE_TYPE"

    async def test_rejects_file_over_10mb(self):
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()
        task = _make_task()
        file = _make_upload_file(size=11 * 1024 * 1024)

        with patch("app.services.attachment_service.plan_task_repository") as repo:
            repo.get_by_id = AsyncMock(return_value=task)
            with pytest.raises(ValidationError) as exc:
                await service.upload_attachment(db, task.id, file, user)
        assert exc.value.code == "FILE_TOO_LARGE"

    async def test_raises_not_found_for_missing_task(self):
        from app.errors import NotFoundError
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()
        file = _make_upload_file()

        with patch("app.services.attachment_service.plan_task_repository") as repo:
            repo.get_by_id = AsyncMock(return_value=None)
            with pytest.raises(NotFoundError):
                await service.upload_attachment(db, uuid.uuid4(), file, user)


class TestDeleteAttachment:

    async def test_rejects_delete_by_other_user(self):
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()
        user.id = uuid.uuid4()

        task_id = uuid.uuid4()
        att = _make_attachment(uploaded_by=uuid.uuid4(), plan_task_id=task_id)

        with patch("app.services.attachment_service.attachment_repository") as repo, \
             patch("app.services.attachment_service.plan_task_repository"):
            repo.get_by_id = AsyncMock(return_value=att)
            with pytest.raises(PermissionError):
                await service.delete_attachment(db, task_id, att.id, user)

    async def test_rejects_delete_after_approval(self):
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()
        user.id = uuid.uuid4()

        task_id = uuid.uuid4()
        att = _make_attachment(uploaded_by=user.id, plan_task_id=task_id)
        task = _make_task(status=OnboardingPlanTaskStatus.APPROVED)

        with patch("app.services.attachment_service.attachment_repository") as att_repo, \
             patch("app.services.attachment_service.plan_task_repository") as task_repo:
            att_repo.get_by_id = AsyncMock(return_value=att)
            task_repo.get_by_id = AsyncMock(return_value=task)
            with pytest.raises(ValidationError) as exc:
                await service.delete_attachment(db, task_id, att.id, user)
        assert exc.value.code == "ATTACHMENT_LOCKED"

    async def test_raises_not_found_for_missing_attachment(self):
        from app.errors import NotFoundError
        service = AttachmentService()
        db = AsyncMock()
        user = MagicMock()

        with patch("app.services.attachment_service.attachment_repository") as repo:
            repo.get_by_id = AsyncMock(return_value=None)
            with pytest.raises(NotFoundError):
                await service.delete_attachment(db, uuid.uuid4(), uuid.uuid4(), user)
