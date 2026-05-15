import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_attachment import TaskAttachment


class TaskAttachmentRepository:

    async def create(self, db: AsyncSession, attachment: TaskAttachment) -> TaskAttachment:
        db.add(attachment)
        return attachment

    async def get_by_id(self, db: AsyncSession, attachment_id: uuid.UUID) -> TaskAttachment | None:
        result = await db.execute(
            select(TaskAttachment).where(
                TaskAttachment.id == attachment_id,
                TaskAttachment.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_task(self, db: AsyncSession, plan_task_id: uuid.UUID) -> list[TaskAttachment]:
        result = await db.execute(
            select(TaskAttachment).where(
                TaskAttachment.plan_task_id == plan_task_id,
                TaskAttachment.deleted_at.is_(None),
            ).order_by(TaskAttachment.created_at)
        )
        return list(result.scalars().all())
