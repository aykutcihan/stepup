from pydantic import BaseModel, computed_field


class DepartmentCompletionRow(BaseModel):
    department_name: str
    total_plans: int
    avg_completion_days: float | None

    @computed_field
    @property
    def avg_completion_days_rounded(self) -> float | None:
        if self.avg_completion_days is None:
            return None
        return round(self.avg_completion_days, 1)


class TemplateCompletionRow(BaseModel):
    template_name: str
    total_tasks: int
    completed_tasks: int

    @computed_field
    @property
    def completion_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(self.completed_tasks / self.total_tasks * 100, 1)


class BottleneckRow(BaseModel):
    task_title: str
    returned_count: int
    overdue_count: int
