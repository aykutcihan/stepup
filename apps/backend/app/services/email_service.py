from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings


class EmailService:

    async def send_invitation_email(self, to_email: str, token: str, role: str) -> None:
        registration_url = f"{settings.FRONTEND_URL}/register?token={token}"
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject="You have been invited to StepUp",
            html_content=f"""
                <p>You have been invited to join StepUp as <strong>{role}</strong>.</p>
                <p><a href="{registration_url}">Click here to complete your registration</a></p>
                <p>This link expires in 7 days.</p>
            """,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)

    async def send_plan_started_email(self, to_email: str, first_name: str) -> None:
        plan_url = f"{settings.FRONTEND_URL}/employee/plan"
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject="Your onboarding plan is ready",
            html_content=f"""
                <p>Hi {first_name},</p>
                <p>Your onboarding plan has been created. You can now view your tasks and get started.</p>
                <p><a href="{plan_url}">View my onboarding plan</a></p>
            """,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)

    async def send_task_completed_email(self, to_email: str, manager_first_name: str, employee_name: str, task_title: str) -> None:
        approvals_url = f"{settings.FRONTEND_URL}/manager/approvals"
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject=f"{employee_name} completed a task — review required",
            html_content=f"""
                <p>Hi {manager_first_name},</p>
                <p><strong>{employee_name}</strong> has marked the following task as complete and it is awaiting your review:</p>
                <p><strong>{task_title}</strong></p>
                <p><a href="{approvals_url}">Go to pending approvals</a></p>
            """,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)

    async def send_task_approved_email(self, to_email: str, first_name: str, task_title: str) -> None:
        plan_url = f"{settings.FRONTEND_URL}/employee/plan"
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject=f"Task approved: {task_title}",
            html_content=f"""
                <p>Hi {first_name},</p>
                <p>Your task has been approved by your manager:</p>
                <p><strong>{task_title}</strong></p>
                <p><a href="{plan_url}">View my onboarding plan</a></p>
            """,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)

    async def send_task_returned_email(self, to_email: str, first_name: str, task_title: str, comment: str) -> None:
        plan_url = f"{settings.FRONTEND_URL}/employee/plan"
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject=f"Task returned for revision: {task_title}",
            html_content=f"""
                <p>Hi {first_name},</p>
                <p>Your manager has returned the following task for revision:</p>
                <p><strong>{task_title}</strong></p>
                <p><strong>Feedback:</strong> {comment}</p>
                <p><a href="{plan_url}">View my onboarding plan</a></p>
            """,
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)
