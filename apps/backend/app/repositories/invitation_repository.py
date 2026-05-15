import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invitation import Invitation


class InvitationRepository:

    async def create(self, db: AsyncSession, invitation: Invitation) -> Invitation:
        db.add(invitation)
        return invitation

    async def get_by_token(self, db: AsyncSession, token: str) -> Invitation | None:
        result = await db.execute(
            select(Invitation).where(Invitation.token == token)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id(self, db: AsyncSession, invitation_id: uuid.UUID) -> Invitation | None:
        result = await db.execute(
            select(Invitation).where(Invitation.id == invitation_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, page: int = 1, page_size: int = 20) -> tuple[list[Invitation], int]:
        now = datetime.now(UTC)
        filters = [
            Invitation.used_at.is_(None),
            Invitation.expires_at > now,
        ]

        count_result = await db.execute(
            select(func.count()).select_from(Invitation).where(*filters)
        )
        total = count_result.scalar_one()

        query = (
            select(Invitation)
            .where(*filters)
            .order_by(Invitation.created_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        result = await db.execute(query)
        return list(result.scalars().all()), total

