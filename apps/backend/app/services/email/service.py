import logging
from pathlib import Path

import httpx
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), autoescape=True)

_SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"
_EXPIRY_DAYS = 7
_REMINDER_DAYS = 2


def _render(template_name: str, **kwargs: str) -> str:
    return _env.get_template(template_name).render(**kwargs)


class EmailService:

    @property
    def _plan_url(self) -> str:
        return f"{settings.FRONTEND_URL}/employee/plan"

    @property
    def _approvals_url(self) -> str:
        return f"{settings.FRONTEND_URL}/manager/approvals"

    @property
    def _register_url(self) -> str:
        return f"{settings.FRONTEND_URL}/register"

    async def _send(self, to_email: str, subject: str, html_content: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                _SENDGRID_URL,
                headers={
                    "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "personalizations": [{"to": [{"email": to_email}]}],
                    "from": {"email": settings.SENDGRID_FROM_EMAIL},
                    "subject": subject,
                    "content": [{"type": "text/html", "value": html_content}],
                },
            )
            response.raise_for_status()

    async def send_invitation_email(self, to_email: str, token: str, role: str) -> None:
        registration_url = f"{self._register_url}?token={token}"
        html = _render(
            "invitation.html",
            registration_url=registration_url,
            role=role,
            expiry_days=str(_EXPIRY_DAYS),
        )
        await self._send(to_email, "You have been invited to StepUp", html)

    async def send_plan_started_email(self, to_email: str, first_name: str) -> None:
        html = _render("plan_started.html", first_name=first_name, plan_url=self._plan_url)
        await self._send(to_email, "Your onboarding plan is ready", html)

    async def send_task_completed_email(
        self, to_email: str, manager_first_name: str, employee_name: str, task_title: str
    ) -> None:
        html = _render(
            "task_completed.html",
            manager_first_name=manager_first_name,
            employee_name=employee_name,
            task_title=task_title,
            approvals_url=self._approvals_url,
        )
        await self._send(to_email, f"{employee_name} completed a task — review required", html)

    async def send_task_approved_email(self, to_email: str, first_name: str, task_title: str) -> None:
        html = _render("task_approved.html", first_name=first_name, task_title=task_title, plan_url=self._plan_url)
        await self._send(to_email, f"Task approved: {task_title}", html)

    async def send_task_returned_email(
        self, to_email: str, first_name: str, task_title: str, comment: str
    ) -> None:
        html = _render(
            "task_returned.html",
            first_name=first_name,
            task_title=task_title,
            comment=comment,
            plan_url=self._plan_url,
        )
        await self._send(to_email, f"Task returned for revision: {task_title}", html)

    async def send_task_overdue_email(
        self, to_email: str, first_name: str, task_title: str, deadline: str
    ) -> None:
        html = _render(
            "task_overdue_employee.html",
            first_name=first_name,
            task_title=task_title,
            deadline=deadline,
            plan_url=self._plan_url,
        )
        await self._send(to_email, f"Task overdue: {task_title}", html)

    async def send_task_overdue_manager_email(
        self, to_email: str, manager_first_name: str, employee_name: str, task_title: str, deadline: str
    ) -> None:
        html = _render(
            "task_overdue_manager.html",
            manager_first_name=manager_first_name,
            employee_name=employee_name,
            task_title=task_title,
            deadline=deadline,
            approvals_url=self._approvals_url,
        )
        await self._send(to_email, f"Overdue task: {task_title} — {employee_name}", html)

    async def send_deadline_reminder_email(
        self, to_email: str, first_name: str, task_title: str, deadline: str
    ) -> None:
        html = _render(
            "deadline_reminder.html",
            first_name=first_name,
            task_title=task_title,
            deadline=deadline,
            reminder_days=str(_REMINDER_DAYS),
            plan_url=self._plan_url,
        )
        await self._send(to_email, f"Reminder: '{task_title}' is due in {_REMINDER_DAYS} days", html)
