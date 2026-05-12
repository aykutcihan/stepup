from fastapi import APIRouter

from app.api.v1 import auth, invitation, user, department, template, onboarding_plan


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(invitation.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(department.router, prefix="/departments", tags=["departments"])
api_router.include_router(template.router, prefix="/templates", tags=["templates"])
api_router.include_router(onboarding_plan.router, prefix="/plans", tags=["plans"])