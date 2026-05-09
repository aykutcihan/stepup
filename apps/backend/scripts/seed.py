import asyncio
import os
import sys
import uuid

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app.enums.user_role import UserRole

DATABASE_URL = os.environ["DATABASE_URL"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SEED_USERS = [
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "email": "admin@stepup.com",
        "password": "Admin1234!",
        "first_name": "HR",
        "last_name": "Admin",
        "role": UserRole.HR_ADMIN,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000002"),
        "email": "manager@stepup.com",
        "password": "Manager1234!",
        "first_name": "Manager",
        "last_name": "User",
        "role": UserRole.MANAGER,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000003"),
        "email": "employee@stepup.com",
        "password": "Employee1234!",
        "first_name": "Employee",
        "last_name": "User",
        "role": UserRole.EMPLOYEE,
    },
]


async def seed():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        for seed_user in SEED_USERS:
            result = await session.execute(
                select(User).where(User.email == seed_user["email"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Seed user already exists: {seed_user['email']}")
                continue

            user = User(
                id=seed_user["id"],
                email=seed_user["email"],
                password_hash=pwd_context.hash(seed_user["password"]),
                first_name=seed_user["first_name"],
                last_name=seed_user["last_name"],
                role=seed_user["role"],
            )
            session.add(user)
            print(f"Seed user created: {seed_user['email']} / {seed_user['password']}")

        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
