from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings


class EmailService:

    async def send_invitation_email(
        self,
        to_email: str,
        token: str,
        role: str,
    ) -> None:
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
