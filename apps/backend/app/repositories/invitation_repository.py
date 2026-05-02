from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invitation import Invitation


class InvitationRepository:

    async def create(self, db: AsyncSession, invitation: Invitation) -> Invitation:
        db.add(invitation)
        await db.commit()
        await db.refresh(invitation)
        return invitation
