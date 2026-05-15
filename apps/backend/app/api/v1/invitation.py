import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
    InvitationValidateResponse,
)
from app.services.invitation_service import InvitationService

router = APIRouter()
invitation_service = InvitationService()


@router.post("/", response_model=InvitationResponse, status_code=201)
async def invite_user(
    data: InvitationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> InvitationResponse:
    invitation = await invitation_service.create_invitation(
        db=db,
        email=data.email,
        role=data.role,
        invited_by=current_user.id,
        department_id=data.department_id,
    )
    return InvitationResponse.model_validate(invitation)

@router.get("/", response_model=list[InvitationResponse], status_code=200)
async def get_invitations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[InvitationResponse]:
    invitations = await invitation_service.get_invitations(db=db)
    result = []
    for inv in invitations:
        result.append(InvitationResponse.model_validate(inv))
    return result

@router.post("/{invitation_id}/resend", response_model=InvitationResponse, status_code=200)
async def resend_invitation(
    invitation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> InvitationResponse:
    invitation = await invitation_service.resend_invitation(
        db=db,
        invitation_id=invitation_id,
    )
    return InvitationResponse.model_validate(invitation)

@router.get("/validate", response_model=InvitationValidateResponse)
async def validate_invitation(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> InvitationValidateResponse:
    invitation = await invitation_service.validate_invitation(db=db, token=token)
    return InvitationValidateResponse(email=invitation.email, role=invitation.role)

