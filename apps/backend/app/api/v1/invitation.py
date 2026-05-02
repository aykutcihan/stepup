import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.invitation import InvitationCreate, InvitationResponse
from app.services.invitation_service import InvitationService

router = APIRouter()
invitation_service = InvitationService()


@router.post("/", response_model=InvitationResponse, status_code=201)
async def invite_user(
    data: InvitationCreate,
    db: AsyncSession = Depends(get_db),
) -> InvitationResponse:
    invitation = await invitation_service.create_invitation(
        db=db,
        email=data.email,
        role=data.role,
        invited_by=uuid.uuid4(),  # TODO: JWT'den gelecek
    )
    return InvitationResponse.model_validate(invitation)
