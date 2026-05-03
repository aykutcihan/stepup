import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.user_role import UserRole
from app.errors import NotFoundError, ValidationError
from app.errors import messages
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


    async def validate_invitation(self, db: AsyncSession, token: str) -> Invitation:
        invitation = await invitation_repository.get_by_token(db, token)

        if invitation is None:
            raise NotFoundError(*messages.INVITATION_NOT_FOUND)

        if invitation.expires_at < datetime.now(timezone.utc):
            raise ValidationError(*messages.INVITATION_EXPIRED)

        if invitation.used_at is not None:
            raise ValidationError(*messages.INVITATION_ALREADY_USED)

        return invitation

    async def mark_invitation_used(self, db: AsyncSession, invitation: Invitation) -> None:
        invitation.used_at = datetime.now(timezone.utc)
        await db.commit()
