from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.dashboard import EmployeeDashboardResponse, HRDashboardResponse, ManagerDashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()


@router.get("/hr", response_model=HRDashboardResponse)
async def get_hr_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> HRDashboardResponse:
    return await dashboard_service.get_hr_stats(db=db)


@router.get("/manager", response_model=ManagerDashboardResponse)
async def get_manager_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.MANAGER)),
) -> ManagerDashboardResponse:
    return await dashboard_service.get_manager_stats(db=db, manager_id=current_user.id)


@router.get("/employee", response_model=EmployeeDashboardResponse)
async def get_employee_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.EMPLOYEE)),
) -> EmployeeDashboardResponse:
    return await dashboard_service.get_employee_stats(db=db, user_id=current_user.id)
