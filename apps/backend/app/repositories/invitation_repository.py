import uuid
from datetime import datetime, timezone

from sqlalchemy import select
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

    async def get_all(self, db: AsyncSession) -> list[Invitation]:
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(Invitation).where(
                Invitation.used_at.is_(None),
                Invitation.expires_at > now,
            )
        )
        return list(result.scalars().all())

