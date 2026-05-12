import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.onboarding_plan import (
    OnboardingPlanCreate,
    OnboardingPlanUpdate,
    OnboardingPlanResponse,
    OnboardingPlanTaskAdd,
    OnboardingPlanTaskUpdate,
    OnboardingPlanTaskResponse,
)
from app.services.onboarding_plan_service import OnboardingPlanService

router = APIRouter()
onboarding_plan_service = OnboardingPlanService()


@router.post("/", response_model=OnboardingPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    data: OnboardingPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanResponse:
    plan = await onboarding_plan_service.create_plan(db=db, data=data)
    return OnboardingPlanResponse.model_validate(plan)


@router.get("/{plan_id}", response_model=OnboardingPlanResponse)
async def get_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanResponse:
    plan = await onboarding_plan_service.get_plan(db=db, plan_id=plan_id)
    return OnboardingPlanResponse.model_validate(plan)


@router.patch("/{plan_id}", response_model=OnboardingPlanResponse)
async def update_plan(
    plan_id: uuid.UUID,
    data: OnboardingPlanUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanResponse:
    plan = await onboarding_plan_service.update_plan(db=db, plan_id=plan_id, data=data)
    return OnboardingPlanResponse.model_validate(plan)


@router.post("/{plan_id}/tasks", response_model=OnboardingPlanTaskResponse, status_code=status.HTTP_201_CREATED)
async def add_task(
    plan_id: uuid.UUID,
    data: OnboardingPlanTaskAdd,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanTaskResponse:
    task = await onboarding_plan_service.add_task(db=db, plan_id=plan_id, data=data)
    return OnboardingPlanTaskResponse.model_validate(task)


@router.patch("/{plan_id}/tasks/{task_id}", response_model=OnboardingPlanTaskResponse)
async def update_task_deadline(
    plan_id: uuid.UUID,
    task_id: uuid.UUID,
    data: OnboardingPlanTaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanTaskResponse:
    task = await onboarding_plan_service.update_task_deadline(db=db, plan_id=plan_id, task_id=task_id, data=data)
    return OnboardingPlanTaskResponse.model_validate(task)


@router.patch("/{plan_id}/tasks/{task_id}/cancel", response_model=OnboardingPlanTaskResponse)
async def cancel_task(
    plan_id: uuid.UUID,
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> OnboardingPlanTaskResponse:
    task = await onboarding_plan_service.cancel_task(db=db, plan_id=plan_id, task_id=task_id)
    return OnboardingPlanTaskResponse.model_validate(task)
