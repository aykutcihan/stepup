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
from app.models.onboarding_template import OnboardingTemplate
from app.models.template_task import TemplateTask
from app.models.user import User
from app.enums.user_role import UserRole

DATABASE_URL = os.environ["DATABASE_URL"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SEED_DEPARTMENTS = [
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000101"), "name": "Engineering"},
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000102"), "name": "Human Resources"},
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000103"), "name": "Product"},
]

SEED_TEMPLATES = [
    {
        "id": uuid.UUID("00000000-0000-0000-0001-000000000001"),
        "name": "Engineering Onboarding",
        "department_id": uuid.UUID("00000000-0000-0000-0000-000000000101"),
        "is_active": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0001-000000000002"),
        "name": "HR Onboarding",
        "department_id": uuid.UUID("00000000-0000-0000-0000-000000000102"),
        "is_active": False,
    },
]

SEED_TASKS = [
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000001"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000001"),
        "title": "Set up development environment",
        "description": "Install required tools: Git, Docker, VS Code, and configure local environment variables.",
        "order": 1,
        "deadline_days": 1,
        "is_required": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000002"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000001"),
        "title": "Complete security and compliance training",
        "description": "Finish the mandatory security awareness course on the learning portal.",
        "order": 2,
        "deadline_days": 3,
        "is_required": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000003"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000001"),
        "title": "Review architecture documentation",
        "description": "Read system design docs and schedule a walkthrough session with the tech lead.",
        "order": 3,
        "deadline_days": 5,
        "is_required": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000004"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000001"),
        "title": "Submit first pull request",
        "description": "Pick a starter task from the backlog, implement it, and open a PR for review.",
        "order": 4,
        "deadline_days": 14,
        "is_required": False,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000005"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000002"),
        "title": "Review HR policies and handbook",
        "description": "Read the company handbook and sign the policy acknowledgement form.",
        "order": 1,
        "deadline_days": 2,
        "is_required": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000006"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000002"),
        "title": "Shadow a payroll processing session",
        "description": "Sit in on the monthly payroll run with a senior HR specialist.",
        "order": 2,
        "deadline_days": 7,
        "is_required": True,
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000007"),
        "template_id": uuid.UUID("00000000-0000-0000-0001-000000000002"),
        "title": "Complete HRIS system training",
        "description": "Finish self-paced training modules for the HR information system.",
        "order": 3,
        "deadline_days": 10,
        "is_required": False,
    },
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

        for seed_tmpl in SEED_TEMPLATES:
            result = await session.execute(
                select(OnboardingTemplate).where(OnboardingTemplate.id == seed_tmpl["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Seed template already exists: {seed_tmpl['name']}")
                continue

            tmpl = OnboardingTemplate(
                id=seed_tmpl["id"],
                name=seed_tmpl["name"],
                department_id=seed_tmpl["department_id"],
                is_active=seed_tmpl["is_active"],
            )
            session.add(tmpl)
            print(f"Seed template created: {seed_tmpl['name']}")

        await session.commit()

        for seed_task in SEED_TASKS:
            result = await session.execute(
                select(TemplateTask).where(TemplateTask.id == seed_task["id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"Seed task already exists: {seed_task['title']}")
                continue

            task = TemplateTask(
                id=seed_task["id"],
                template_id=seed_task["template_id"],
                title=seed_task["title"],
                description=seed_task["description"],
                order=seed_task["order"],
                deadline_days=seed_task["deadline_days"],
                is_required=seed_task["is_required"],
            )
            session.add(task)
            print(f"Seed task created: {seed_task['title']}")

        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
