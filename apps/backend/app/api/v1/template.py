from typing import Optional
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.template import TemplateCreate, TemplateResponse, TemplateUpdate, TaskCreate, TaskUpdate, TaskResponse
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


@router.patch("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: uuid.UUID,
    data: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TemplateResponse:
    template = await template_service.update_template(
        db=db, template_id=template_id, data=data
    )
    return TemplateResponse.model_validate(template)

@router.patch("/{template_id}/activate", response_model=TemplateResponse)
async def activate_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TemplateResponse:
    template = await template_service.activate_template(db=db, template_id=template_id)
    return TemplateResponse.model_validate(template)


@router.patch("/{template_id}/deactivate", response_model=TemplateResponse)
async def deactivate_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TemplateResponse:
    template = await template_service.deactivate_template(db=db, template_id=template_id)
    return TemplateResponse.model_validate(template)


@router.post("/{template_id}/clone", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def clone_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TemplateResponse:
    template = await template_service.clone_template(db=db, template_id=template_id)
    return TemplateResponse.model_validate(template)


@router.post("/{template_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def add_task(
    template_id: uuid.UUID,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TaskResponse:
    task = await template_service.add_task(db=db, template_id=template_id, data=data)
    return TaskResponse.model_validate(task)


@router.delete("/{template_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    template_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> None:
    await template_service.delete_task(
        db=db, template_id=template_id, task_id=task_id
    )


@router.patch("/{template_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    template_id: uuid.UUID,
    task_id: uuid.UUID,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> TaskResponse:
    task = await template_service.update_task(
        db=db, template_id=template_id, task_id=task_id, data=data
    )
    return TaskResponse.model_validate(task)


@router.get("/{template_id}/tasks", response_model=list[TaskResponse])
async def get_tasks(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[TaskResponse]:
    tasks = await template_service.get_tasks(db=db, template_id=template_id)
    return [TaskResponse.model_validate(t) for t in tasks]

