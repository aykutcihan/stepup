import asyncio
import os
import sys
import uuid

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.department import Department
from app.models.user import User
from app.enums.user_role import UserRole

DATABASE_URL = os.environ["DATABASE_URL"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SEED_DEPARTMENTS = [
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000101"), "name": "Engineering"},
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000102"), "name": "Human Resources"},
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000103"), "name": "Product"},
]

SEED_USERS = [
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "email": "admin@stepup.com",
        "password": "Admin1234!",
        "first_name": "HR",
        "last_name": "Admin",
        "role": UserRole.HR_ADMIN,
        "department_id": uuid.UUID("00000000-0000-0000-0000-000000000102"),
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000002"),
        "email": "manager@stepup.com",
        "password": "Manager1234!",
        "first_name": "Manager",
        "last_name": "User",
        "role": UserRole.MANAGER,
        "department_id": uuid.UUID("00000000-0000-0000-0000-000000000101"),
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0000-000000000003"),
        "email": "employee@stepup.com",
        "password": "Employee1234!",
        "first_name": "Employee",
        "last_name": "User",
        "role": UserRole.EMPLOYEE,
        "department_id": uuid.UUID("00000000-0000-0000-0000-000000000101"),
    },
]


async def seed():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        for seed_dept in SEED_DEPARTMENTS:
            result = await session.execute(
                select(Department).where(Department.id == seed_dept["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Seed department already exists: {seed_dept['name']}")
                continue

            dept = Department(id=seed_dept["id"], name=seed_dept["name"])
            session.add(dept)
            print(f"Seed department created: {seed_dept['name']}")

        await session.commit()

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
                department_id=seed_user["department_id"],
            )
            session.add(user)
            print(f"Seed user created: {seed_user['email']} / {seed_user['password']}")

        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
