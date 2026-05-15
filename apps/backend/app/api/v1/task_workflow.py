import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.onboarding_plan import (
    ApprovalTaskResponse,
    OnboardingPlanResponse,
    OnboardingPlanTaskResponse,
    ReturnTask,
)
from app.services.task_workflow_service import TaskWorkflowService

plans_router = APIRouter()
tasks_router = APIRouter()
manager_router = APIRouter()
task_workflow_service = TaskWorkflowService()


@plans_router.get("/me", response_model=OnboardingPlanResponse)
async def get_my_plan(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYEE)),
) -> OnboardingPlanResponse:
    plan = await task_workflow_service.get_my_plan(db=db, current_user=current_user)
    return OnboardingPlanResponse.model_validate(plan)


@tasks_router.patch("/{task_id}/start", response_model=OnboardingPlanTaskResponse)
async def start_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYEE)),
) -> OnboardingPlanTaskResponse:
    task = await task_workflow_service.start_task(db=db, task_id=task_id, current_user=current_user)
    return OnboardingPlanTaskResponse.model_validate(task)


@tasks_router.patch("/{task_id}/complete", response_model=OnboardingPlanTaskResponse)
async def complete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYEE)),
) -> OnboardingPlanTaskResponse:
    task = await task_workflow_service.complete_task(db=db, task_id=task_id, current_user=current_user)
    return OnboardingPlanTaskResponse.model_validate(task)


@manager_router.get("/approvals", response_model=list[ApprovalTaskResponse])
async def get_pending_approvals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER)),
) -> list[ApprovalTaskResponse]:
    return await task_workflow_service.get_pending_approvals(db=db, current_user=current_user)


@tasks_router.patch("/{task_id}/approve", response_model=OnboardingPlanTaskResponse)
async def approve_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER)),
) -> OnboardingPlanTaskResponse:
    task = await task_workflow_service.approve_task(db=db, task_id=task_id, current_user=current_user)
    return OnboardingPlanTaskResponse.model_validate(task)


@tasks_router.patch("/{task_id}/return", response_model=OnboardingPlanTaskResponse)
async def return_task(
    task_id: uuid.UUID,
    data: ReturnTask,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER)),
) -> OnboardingPlanTaskResponse:
    task = await task_workflow_service.return_task(db=db, task_id=task_id, current_user=current_user, data=data)
    return OnboardingPlanTaskResponse.model_validate(task)
