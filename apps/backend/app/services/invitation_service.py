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
from app.services.email_service import EmailService

INVITATION_EXPIRY_DAYS = 7

invitation_repository = InvitationRepository()
user_repository = UserRepository()
email_service = EmailService()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InvitationService:

    async def create_invitation(
        self,
        db: AsyncSession,
        email: str,
        role: UserRole,
        invited_by: uuid.UUID,
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
        )
        await invitation_repository.create(db, invitation)
        await db.commit()
        await db.refresh(invitation)
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

        existing_user = await user_repository.get_by_email(db, email)
        if existing_user:
            raise ValidationError(*messages.USER_ALREADY_EXISTS)

        user = User(
            email=invitation.email,
            role=invitation.role,
            first_name=first_name,
            last_name=last_name,
            password_hash=pwd_context.hash(password),
        )
        db.add(user)
        invitation.used_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user
