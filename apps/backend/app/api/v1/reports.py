from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.enums.user_role import UserRole
from app.models.user import User
from app.schemas.reports import (
    BottleneckRow,
    DepartmentCompletionRow,
    TemplateCompletionRow,
)
from app.services.reports_service import ReportsService

router = APIRouter()
reports_service = ReportsService()


@router.get("/completion-time", response_model=list[DepartmentCompletionRow])
async def get_completion_time(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    format: str = Query("json", pattern="^(json|csv)$"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[DepartmentCompletionRow] | StreamingResponse:
    rows = await reports_service.get_completion_time(db, start_date, end_date)
    if format == "csv":
        headers = ["department_name", "total_plans", "avg_completion_days"]
        csv_data = reports_service.to_csv(headers, [r.model_dump() for r in rows])
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=completion-time.csv"},
        )
    return rows


@router.get("/task-completion-rates", response_model=list[TemplateCompletionRow])
async def get_task_completion_rates(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    format: str = Query("json", pattern="^(json|csv)$"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[TemplateCompletionRow] | StreamingResponse:
    rows = await reports_service.get_task_completion_rates(db, start_date, end_date)
    if format == "csv":
        headers = ["template_name", "total_tasks", "completed_tasks", "completion_rate"]
        csv_data = reports_service.to_csv(headers, [r.model_dump() for r in rows])
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=task-completion-rates.csv"},
        )
    return rows


@router.get("/bottlenecks", response_model=list[BottleneckRow])
async def get_bottlenecks(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    format: str = Query("json", pattern="^(json|csv)$"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.HR_ADMIN)),
) -> list[BottleneckRow] | StreamingResponse:
    rows = await reports_service.get_bottlenecks(db, start_date, end_date)
    if format == "csv":
        headers = ["task_title", "returned_count", "overdue_count"]
        csv_data = reports_service.to_csv(headers, [r.model_dump() for r in rows])
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=bottlenecks.csv"},
        )
    return rows
