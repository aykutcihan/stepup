import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.user_role import UserRole
from app.models.invitation import Invitation
from app.repositories.invitation_repository import InvitationRepository
from app.services.email_service import EmailService

INVITATION_EXPIRY_DAYS = 7

invitation_repository = InvitationRepository()
email_service = EmailService()


class InvitationService:

    async def create_invitation(
        self,
        db: AsyncSession,
        email: str,
        role: UserRole,
        invited_by: uuid.UUID,
    ) -> Invitation:
        invitation = Invitation(
            email=email,
            role=role,
            token=secrets.token_urlsafe(32),
            invited_by=invited_by,
            expires_at=datetime.now(timezone.utc) + timedelta(days=INVITATION_EXPIRY_DAYS),
        )
        await invitation_repository.create(db, invitation)
        await email_service.send_invitation_email(
            to_email=email,
            token=invitation.token,
            role=role.value,
        )
        return invitation
