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
