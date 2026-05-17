import asyncio
import os
import sys

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app.models  # noqa

from app.enums.user_role import UserRole
from app.models.user import User

DATABASE_URL = os.environ["DATABASE_URL"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        users = [
            User(
                email="admin@stepup.com",
                password_hash=pwd_context.hash("Admin1234!"),
                first_name="Admin",
                last_name="User",
                role=UserRole.HR_ADMIN,
            ),
            User(
                email="manager@stepup.com",
                password_hash=pwd_context.hash("Manager1234!"),
                first_name="Manager",
                last_name="User",
                role=UserRole.MANAGER,
            ),
            User(
                email="employee@stepup.com",
                password_hash=pwd_context.hash("Employee1234!"),
                first_name="Employee",
                last_name="User",
                role=UserRole.EMPLOYEE,
            ),
        ]
        session.add_all(users)
        await session.commit()
        print(f"Seeded {len(users)} users.")


if __name__ == "__main__":
    asyncio.run(seed())
