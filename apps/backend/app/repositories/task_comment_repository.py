import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_comment import TaskComment


class TaskCommentRepository:

    async def create(self, db: AsyncSession, comment: TaskComment) -> TaskComment:
        db.add(comment)
        return comment

    async def get_by_task(self, db: AsyncSession, plan_task_id: uuid.UUID) -> list[TaskComment]:
        result = await db.execute(
            select(TaskComment).where(
                TaskComment.plan_task_id == plan_task_id,
                TaskComment.deleted_at.is_(None),
            ).order_by(TaskComment.created_at)
        )
        return list(result.scalars().all())
