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
