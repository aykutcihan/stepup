from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.template import TemplateCreate, TemplateResponse
from app.services.template_service import TemplateService

router = APIRouter()
template_service = TemplateService()

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    data: TemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TemplateResponse:
    template = await template_service.create_template(db=db, data=data)
    return TemplateResponse.model_validate(template)