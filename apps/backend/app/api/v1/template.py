from typing import Optional
import uuid

from fastapi import APIRouter, Depends, Query, status
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

@router.get("/", response_model=list[TemplateResponse])
async def get_templates(
    department_id: Optional[uuid.UUID] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[TemplateResponse]:
    templates = await template_service.get_all_templates(
        db=db, department_id=department_id, is_active=is_active
    )
    
    response_list = []

    for t in templates:
        validated_data = TemplateResponse.model_validate(t)
        response_list.append(validated_data)

    return response_list