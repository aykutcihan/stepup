import csv
import io
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.reports_repository import ReportsRepository
from app.schemas.reports import DepartmentCompletionRow, TemplateCompletionRow, BottleneckRow

reports_repository = ReportsRepository()


class ReportsService:

    async def get_completion_time(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[DepartmentCompletionRow]:
        rows = await reports_repository.get_completion_time_by_department(
            db, start_date, end_date
        )
        return [DepartmentCompletionRow(**r) for r in rows]

    async def get_task_completion_rates(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[TemplateCompletionRow]:
        rows = await reports_repository.get_task_completion_rates(db, start_date, end_date)
        return [TemplateCompletionRow(**r) for r in rows]

    async def get_bottlenecks(
        self,
        db: AsyncSession,
        start_date: date | None,
        end_date: date | None,
    ) -> list[BottleneckRow]:
        rows = await reports_repository.get_bottlenecks(db, start_date, end_date)
        return [BottleneckRow(**r) for r in rows]

    def to_csv(self, headers: list[str], rows: list[dict]) -> str:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
        return buf.getvalue()
