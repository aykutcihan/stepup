from sqlalchemy.ext.asyncio import AsyncSession
from app.models.onboarding_template import OnboardingTemplate

class TemplateRepository:
    async def create(
        self, db: AsyncSession, template: OnboardingTemplate
    ) -> OnboardingTemplate:
        db.add(template)
        return template