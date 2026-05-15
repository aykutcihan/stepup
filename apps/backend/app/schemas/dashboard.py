from datetime import date
from pydantic import BaseModel


class HRDashboardResponse(BaseModel):
    active_users: int
    active_plans: int
    active_departments: int
    pending_approvals: int


class ManagerDashboardResponse(BaseModel):
    active_plans: int
    pending_approvals: int
    total_employees: int


class EmployeeDashboardResponse(BaseModel):
    total_tasks: int
    approved_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    next_deadline: date | None
