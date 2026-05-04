import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    async def create(self, db: AsyncSession, refresh_token: RefreshToken) -> RefreshToken:
        db.add(refresh_token)
        return refresh_token

    async def get_by_token(self, db: AsyncSession, token: str) -> RefreshToken | None:
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()

    async def delete_by_user_id(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        await db.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )

    async def delete_by_token(self, db: AsyncSession, token: str) -> None:
        await db.execute(
            delete(RefreshToken).where(RefreshToken.token == token)
        )
