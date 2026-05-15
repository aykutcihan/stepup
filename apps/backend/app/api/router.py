from fastapi import APIRouter

from app.api.v1 import (
    attachments,
    audit,
    auth,
    dashboard,
    department,
    invitation,
    onboarding_plan,
    reports,
    task_workflow,
    template,
    user,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(invitation.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(department.router, prefix="/departments", tags=["departments"])
api_router.include_router(template.router, prefix="/templates", tags=["templates"])
api_router.include_router(task_workflow.plans_router, prefix="/plans", tags=["employee-tasks"])
api_router.include_router(onboarding_plan.router, prefix="/plans", tags=["plans"])
api_router.include_router(task_workflow.tasks_router, prefix="/tasks", tags=["employee-tasks"])
api_router.include_router(task_workflow.manager_router, prefix="/manager", tags=["manager-tasks"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(attachments.router, prefix="/tasks", tags=["attachments"])