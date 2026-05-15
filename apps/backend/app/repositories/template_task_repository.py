import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template_task import TemplateTask


class TemplateTaskRepository:

    async def get_by_template(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> list[TemplateTask]:
        result = await db.execute(
            select(TemplateTask).where(
                TemplateTask.template_id == template_id,
                TemplateTask.deleted_at.is_(None),
            ).order_by(TemplateTask.order)
        )
        return list(result.scalars().all())

    async def get_max_order(
        self, db: AsyncSession, template_id: uuid.UUID
    ) -> int:
        from sqlalchemy import func
        result = await db.execute(
            select(func.max(TemplateTask.order)).where(
                TemplateTask.template_id == template_id,
                TemplateTask.deleted_at.is_(None),
            )
        )
        return result.scalar_one() or 0

    async def get_by_id(
        self, db: AsyncSession, task_id: uuid.UUID
    ) -> TemplateTask | None:
        result = await db.execute(
            select(TemplateTask).where(
                TemplateTask.id == task_id,
                TemplateTask.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self, db: AsyncSession, task: TemplateTask
    ) -> TemplateTask:
        db.add(task)
        return task
