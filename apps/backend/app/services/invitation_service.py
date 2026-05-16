import logging
import secrets
import uuid
from datetime import UTC, datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.audit_enums import AuditActionType, AuditEntityType
from app.enums.user_role import UserRole
from app.errors import NotFoundError, ValidationError, messages
from app.models.invitation import Invitation
from app.models.user import User
from app.repositories.invitation_repository import InvitationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.invitation import InvitationListResponse, InvitationResponse
from app.services.audit_service import AuditService
from app.services.email_service import EmailService

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
            expires_at=datetime.now(UTC) + timedelta(days=INVITATION_EXPIRY_DAYS),
            department_id=department_id,
        )
        await invitation_repository.create(db, invitation)
        await db.flush()
        await audit_service.log(db, actor_id=invited_by, action=AuditActionType.user_invited, entity_type=AuditEntityType.invitation, entity_id=invitation.id, detail=email)
        await db.commit()
        await db.refresh(invitation)

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

        if invitation.expires_at < datetime.now(UTC):
            raise ValidationError(*messages.INVITATION_EXPIRED)

        if invitation.used_at is not None:
            raise ValidationError(*messages.INVITATION_ALREADY_USED)

        return invitation

    async def mark_invitation_used(self, invitation: Invitation) -> None:
        invitation.used_at = datetime.now(UTC)

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
        invitation.used_at = datetime.now(UTC)
        await db.flush()
        await audit_service.log(db, actor_id=user.id, action=AuditActionType.user_registered, entity_type=AuditEntityType.user, entity_id=user.id)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def get_invitations(self, db: AsyncSession, page: int = 1, page_size: int = 20) -> InvitationListResponse:
        items, total = await invitation_repository.get_all(db, page=page, page_size=page_size)
        total_pages = (total + page_size - 1) // page_size
        return InvitationListResponse(
            items=[InvitationResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page * page_size < total,
            has_prev=page > 1,
        )

    async def resend_invitation(
        self,
        db: AsyncSession,
        invitation_id: uuid.UUID,
        actor_id: uuid.UUID,
    ) -> Invitation:
        invitation = await invitation_repository.get_by_id(db, invitation_id)
        if not invitation:
            raise NotFoundError(*messages.INVITATION_NOT_FOUND)

        if invitation.used_at is not None:
            raise ValidationError(*messages.INVITATION_ALREADY_USED)

        invitation.token = secrets.token_urlsafe(32)
        invitation.expires_at = datetime.now(UTC) + timedelta(days=INVITATION_EXPIRY_DAYS)
        await audit_service.log(db, actor_id=actor_id, action=AuditActionType.user_invitation_resent, entity_type=AuditEntityType.invitation, entity_id=invitation_id, detail=invitation.email)
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
 