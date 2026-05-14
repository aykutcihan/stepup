import uuid
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus


class ReturnTask(BaseModel):
    content: str


class ApprovalTaskResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    title: str
    description: str | None
    deadline: date
    status: OnboardingPlanTaskStatus
    is_required: bool
    order: int
    created_at: datetime
    employee_name: str
    plan_start_date: date


class OnboardingPlanCreate(BaseModel):
    user_id: uuid.UUID
    template_id: uuid.UUID
    manager_id: uuid.UUID
    start_date: date


class OnboardingPlanUpdate(BaseModel):
    manager_id: uuid.UUID | None = None


class OnboardingPlanTaskUpdate(BaseModel):
    deadline: date


class OnboardingPlanTaskAdd(BaseModel):
    title: str
    description: str | None = None
    deadline: date
    is_required: bool = True


class OnboardingPlanTaskResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    template_task_id: uuid.UUID | None
    title: str
    description: str | None
    deadline: date
    status: OnboardingPlanTaskStatus
    is_required: bool
    order: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OnboardingPlanResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    template_id: uuid.UUID
    manager_id: uuid.UUID
    start_date: date
    is_active: bool
    created_at: datetime
    tasks: list[OnboardingPlanTaskResponse]

    model_config = ConfigDict(from_attributes=True)
