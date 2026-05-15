import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


class AuditLogRepository:

    async def create(self, db: AsyncSession, log: AuditLog) -> None:
        db.add(log)

    async def get_all(
        self,
        db: AsyncSession,
        action: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditLog]:
        query = select(AuditLog).order_by(AuditLog.created_at.desc())
        if action:
            query = query.where(AuditLog.action == action)
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return list(result.scalars().all())
