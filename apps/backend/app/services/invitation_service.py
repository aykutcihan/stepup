import secrets
import uuid
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.user_role import UserRole
from app.errors import NotFoundError, ValidationError
from app.errors import messages
from app.models.invitation import Invitation
from app.models.user import User
from app.repositories.invitation_repository import InvitationRepository
from app.repositories.user_repository import UserRepository
from app.services.audit_service import AuditService
from app.services.email_service import EmailService

import logging

logger = logging.getLogger(__name__)

INVITATION_EXPIRY_DAYS = 7

invitation_repository = InvitationRepository()
user_repository = UserRepository()
email_service = EmailService()
audit_service = AuditService()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InvitationService:

    async def create_invitation(
        self,
        db: AsyncSession,
        email: str,
        role: UserRole,
        invited_by: uuid.UUID,
        department_id: uuid.UUID | None = None,
    ) -> Invitation:
        existing_user = await user_repository.get_by_email(db, email)
        if existing_user:
            raise ValidationError(*messages.USER_ALREADY_EXISTS)

        invitation = Invitation(
            email=email,
            role=role,
            token=secrets.token_urlsafe(32),
            invited_by=invited_by,
            expires_at=datetime.now(timezone.utc) + timedelta(days=INVITATION_EXPIRY_DAYS),
            department_id=department_id,
        )
        await invitation_repository.create(db, invitation)
        await db.commit()
        await db.refresh(invitation)
        await audit_service.log(db, actor_id=invited_by, action="user.invited", entity_type="invitation", entity_id=invitation.id, detail=email)
        await db.commit()

        try:
            await email_service.send_invitation_email(
                to_email=email,
                token=invitation.token,
                role=role.value,
            )
        except Exception as e:
            logger.error(f"Failed to send invitation email to {email}: {e}")

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

    async def mark_invitation_used(self, invitation: Invitation) -> None:
        invitation.used_at = datetime.now(timezone.utc)

    async def register_user_from_invitation(
        self,
        db: AsyncSession,
        token: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> User:
        invitation = await self.validate_invitation(db, token)

        existing_user = await user_repository.get_by_email(db, invitation.email)
        if existing_user:
            raise ValidationError(*messages.USER_ALREADY_EXISTS)

        user = User(
            email=invitation.email,
            role=invitation.role,
            first_name=first_name,
            last_name=last_name,
            password_hash=pwd_context.hash(password),
            department_id=invitation.department_id,
        )
        db.add(user)
        invitation.used_at = datetime.now(timezone.utc)
        await db.flush()
        await db.commit()
        await db.refresh(user)
        await audit_service.log(db, actor_id=user.id, action="user.registered", entity_type="user", entity_id=user.id)
        await db.commit()
        return user
    
    async def get_invitations(self, db: AsyncSession) -> list[Invitation]:
        return await invitation_repository.get_all(db)

    async def resend_invitation(
        self,
        db: AsyncSession,
        invitation_id: uuid.UUID,
    ) -> Invitation:
        invitation = await invitation_repository.get_by_id(db, invitation_id)
        if not invitation:
            raise NotFoundError(*messages.INVITATION_NOT_FOUND)

        if invitation.used_at is not None:
            raise ValidationError(*messages.INVITATION_ALREADY_USED)

        invitation.token = secrets.token_urlsafe(32)
        invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=INVITATION_EXPIRY_DAYS)
        await db.commit()
        await db.refresh(invitation)

        try:
            await email_service.send_invitation_email(
                to_email=invitation.email,
                token=invitation.token,
                role=invitation.role.value,
            )
        except Exception as e:
            logger.error(f"Failed to resend invitation email to {invitation.email}: {e}")

        return invitation
 