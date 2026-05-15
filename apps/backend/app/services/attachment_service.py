import uuid

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.errors import NotFoundError, PermissionError, ValidationError, messages
from app.models.task_attachment import TaskAttachment
from app.models.task_comment import TaskComment
from app.models.user import User
from app.repositories.onboarding_plan_task_repository import (
    OnboardingPlanTaskRepository,
)
from app.repositories.task_attachment_repository import TaskAttachmentRepository
from app.repositories.task_comment_repository import TaskCommentRepository
from app.schemas.attachment import (
    TaskAttachmentResponse,
    TaskCommentCreate,
    TaskCommentResponse,
)
from app.services.storage_service import (
    ALLOWED_CONTENT_TYPES,
    MAX_FILE_SIZE,
    StorageService,
)

plan_task_repository = OnboardingPlanTaskRepository()
attachment_repository = TaskAttachmentRepository()
comment_repository = TaskCommentRepository()
storage_service = StorageService()


class AttachmentService:

    async def upload_attachment(
        self,
        db: AsyncSession,
        task_id: uuid.UUID,
        file: UploadFile,
        current_user: User,
    ) -> TaskAttachmentResponse:
        task = await plan_task_repository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError(*messages.INVALID_FILE_TYPE)

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise ValidationError(*messages.FILE_TOO_LARGE)

        object_name = f"tasks/{task_id}/{uuid.uuid4()}_{file.filename}"
        storage_service.upload(content, object_name, file.content_type)

        attachment = TaskAttachment(
            plan_task_id=task_id,
            uploaded_by=current_user.id,
            file_name=file.filename,
            object_name=object_name,
            file_type=file.content_type,
            file_size=len(content),
        )
        await attachment_repository.create(db, attachment)
        await db.commit()
        await db.refresh(attachment)

        return self._to_response(attachment)

    async def delete_attachment(
        self,
        db: AsyncSession,
        task_id: uuid.UUID,
        attachment_id: uuid.UUID,
        current_user: User,
    ) -> None:
        attachment = await attachment_repository.get_by_id(db, attachment_id)
        if not attachment or attachment.plan_task_id != task_id:
            raise NotFoundError(*messages.ATTACHMENT_NOT_FOUND)

        if attachment.uploaded_by != current_user.id:
            raise PermissionError(*messages.PERMISSION_DENIED)

        task = await plan_task_repository.get_by_id(db, task_id)
        if task and task.status == OnboardingPlanTaskStatus.APPROVED:
            raise ValidationError(*messages.ATTACHMENT_LOCKED)

        storage_service.delete(attachment.object_name)
        await db.delete(attachment)
        await db.commit()

    async def add_comment(
        self,
        db: AsyncSession,
        task_id: uuid.UUID,
        data: TaskCommentCreate,
        current_user: User,
    ) -> TaskCommentResponse:
        task = await plan_task_repository.get_by_id(db, task_id)
        if not task:
            raise NotFoundError(*messages.PLAN_TASK_NOT_FOUND)

        comment = TaskComment(
            plan_task_id=task_id,
            user_id=current_user.id,
            content=data.content,
        )
        await comment_repository.create(db, comment)
        await db.commit()
        await db.refresh(comment)

        return TaskCommentResponse.model_validate(comment)

    def _to_response(self, attachment: TaskAttachment) -> TaskAttachmentResponse:
        download_url = storage_service.signed_url(attachment.object_name)
        return TaskAttachmentResponse(
            id=attachment.id,
            plan_task_id=attachment.plan_task_id,
            uploaded_by=attachment.uploaded_by,
            file_name=attachment.file_name,
            file_type=attachment.file_type,
            file_size=attachment.file_size,
            download_url=download_url,
            created_at=attachment.created_at,
        )
