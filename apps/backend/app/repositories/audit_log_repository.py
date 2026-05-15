import uuid
from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.models.audit_log import AuditLog


class AuditLogRepository:

    async def create(self, db: AsyncSession, log: AuditLog) -> None:
        db.add(log)

    async def get_all(
        self,
        db: AsyncSession,
        action: AuditActionType | None = None,
        entity_type: AuditEntityType | None = None,
        actor_id: uuid.UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[AuditLog], int]:
        filters = []

        if action:
            filters.append(AuditLog.action == action)
        if entity_type:
            filters.append(AuditLog.entity_type == entity_type)
        if actor_id:
            filters.append(AuditLog.actor_id == actor_id)
        if date_from:
            filters.append(AuditLog.created_at >= date_from)
        if date_to:
            filters.append(AuditLog.created_at <= date_to)

        count_query = select(func.count()).select_from(AuditLog)
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = await db.execute(count_query)
        total = count_result.scalar_one()

        offset = (page - 1) * page_size
        query = select(AuditLog)
        if filters:
            query = query.where(and_(*filters))
        query = query.order_by(AuditLog.created_at.desc()).limit(page_size).offset(offset)

        result = await db.execute(query)
        items = list(result.scalars().all())

        return items, total
