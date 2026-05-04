import asyncio
import uuid
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app.enums.user_role import UserRole
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

HR_ADMIN = {
    "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
    "email": "admin@stepup.com",
    "password": "Admin1234!",
    "first_name": "HR",
    "last_name": "Admin",
    "role": UserRole.HR_ADMIN,
}


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.email == HR_ADMIN["email"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Seed user already exists: {HR_ADMIN['email']}")
            return

        user = User(
            id=HR_ADMIN["id"],
            email=HR_ADMIN["email"],
            password_hash=pwd_context.hash(HR_ADMIN["password"]),
            first_name=HR_ADMIN["first_name"],
            last_name=HR_ADMIN["last_name"],
            role=HR_ADMIN["role"],
        )
        session.add(user)
        await session.commit()
        print(f"Seed user created: {HR_ADMIN['email']} / {HR_ADMIN['password']}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
