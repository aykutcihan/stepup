import asyncio
import os
import sys
import uuid
from datetime import date, timedelta

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app.models  # noqa — ensures all models are registered with Base

from app.models.audit_log import AuditLog
from app.models.department import Department
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.onboarding_template import OnboardingTemplate
from app.models.template_task import TemplateTask
from app.models.user import User
from app.enums.user_role import UserRole
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus

DATABASE_URL = os.environ["DATABASE_URL"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TODAY = date.today()

# ─── Fixed IDs ────────────────────────────────────────────────────────────────

ADMIN_ID     = uuid.UUID("00000000-0000-0000-0000-000000000001")
MANAGER_ID   = uuid.UUID("00000000-0000-0000-0000-000000000002")
EMPLOYEE_ID  = uuid.UUID("00000000-0000-0000-0000-000000000003")
ALICE_ID     = uuid.UUID("00000000-0000-0000-0000-000000000004")
BOB_ID       = uuid.UUID("00000000-0000-0000-0000-000000000005")
MANAGER2_ID  = uuid.UUID("00000000-0000-0000-0000-000000000006")

DEPT_ENG_ID  = uuid.UUID("00000000-0000-0000-0000-000000000101")
DEPT_HR_ID   = uuid.UUID("00000000-0000-0000-0000-000000000102")
DEPT_PROD_ID = uuid.UUID("00000000-0000-0000-0000-000000000103")

TMPL_ENG_ID  = uuid.UUID("00000000-0000-0000-0001-000000000001")
TMPL_HR_ID   = uuid.UUID("00000000-0000-0000-0001-000000000002")
TMPL_PROD_ID = uuid.UUID("00000000-0000-0000-0001-000000000003")

PLAN_EMP_ID   = uuid.UUID("00000000-0000-0000-0003-000000000001")
PLAN_ALICE_ID = uuid.UUID("00000000-0000-0000-0003-000000000002")
PLAN_BOB_ID   = uuid.UUID("00000000-0000-0000-0003-000000000003")

# ─── Departments ──────────────────────────────────────────────────────────────

SEED_DEPARTMENTS = [
    {"id": DEPT_ENG_ID,  "name": "Engineering"},
    {"id": DEPT_HR_ID,   "name": "Human Resources"},
    {"id": DEPT_PROD_ID, "name": "Product"},
]

# ─── Users ────────────────────────────────────────────────────────────────────

SEED_USERS = [
    {
        "id": ADMIN_ID, "email": "admin@stepup.com", "password": "Admin1234!",
        "first_name": "HR", "last_name": "Admin",
        "role": UserRole.HR_ADMIN, "department_id": DEPT_HR_ID,
    },
    {
        "id": MANAGER_ID, "email": "manager@stepup.com", "password": "Manager1234!",
        "first_name": "Alex", "last_name": "Manager",
        "role": UserRole.MANAGER, "department_id": DEPT_ENG_ID,
    },
    {
        "id": MANAGER2_ID, "email": "manager2@stepup.com", "password": "Manager1234!",
        "first_name": "Sam", "last_name": "Lead",
        "role": UserRole.MANAGER, "department_id": DEPT_PROD_ID,
    },
    {
        "id": EMPLOYEE_ID, "email": "employee@stepup.com", "password": "Employee1234!",
        "first_name": "John", "last_name": "Doe",
        "role": UserRole.EMPLOYEE, "department_id": DEPT_ENG_ID,
    },
    {
        "id": ALICE_ID, "email": "alice@stepup.com", "password": "Employee1234!",
        "first_name": "Alice", "last_name": "Chen",
        "role": UserRole.EMPLOYEE, "department_id": DEPT_ENG_ID,
    },
    {
        "id": BOB_ID, "email": "bob@stepup.com", "password": "Employee1234!",
        "first_name": "Bob", "last_name": "Marley",
        "role": UserRole.EMPLOYEE, "department_id": DEPT_PROD_ID,
    },
]

# ─── Templates ────────────────────────────────────────────────────────────────

SEED_TEMPLATES = [
    {"id": TMPL_ENG_ID,  "name": "Engineering Onboarding", "department_id": DEPT_ENG_ID,  "is_active": True},
    {"id": TMPL_HR_ID,   "name": "HR Onboarding",          "department_id": DEPT_HR_ID,   "is_active": False},
    {"id": TMPL_PROD_ID, "name": "Product Onboarding",     "department_id": DEPT_PROD_ID, "is_active": True},
]

# ─── Template Tasks ───────────────────────────────────────────────────────────

SEED_TEMPLATE_TASKS = [
    # Engineering Onboarding
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000001"),
        "template_id": TMPL_ENG_ID, "order": 1, "deadline_days": 1, "is_required": True,
        "title": "Set up development environment",
        "description": "Install required tools: Git, Docker, VS Code, and configure local environment variables.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000002"),
        "template_id": TMPL_ENG_ID, "order": 2, "deadline_days": 3, "is_required": True,
        "title": "Complete security and compliance training",
        "description": "Finish the mandatory security awareness course on the learning portal.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000003"),
        "template_id": TMPL_ENG_ID, "order": 3, "deadline_days": 5, "is_required": True,
        "title": "Review architecture documentation",
        "description": "Read system design docs and schedule a walkthrough session with the tech lead.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000004"),
        "template_id": TMPL_ENG_ID, "order": 4, "deadline_days": 14, "is_required": False,
        "title": "Submit first pull request",
        "description": "Pick a starter task from the backlog, implement it, and open a PR for review.",
    },
    # HR Onboarding
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000005"),
        "template_id": TMPL_HR_ID, "order": 1, "deadline_days": 2, "is_required": True,
        "title": "Review HR policies and handbook",
        "description": "Read the company handbook and sign the policy acknowledgement form.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000006"),
        "template_id": TMPL_HR_ID, "order": 2, "deadline_days": 7, "is_required": True,
        "title": "Shadow a payroll processing session",
        "description": "Sit in on the monthly payroll run with a senior HR specialist.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000007"),
        "template_id": TMPL_HR_ID, "order": 3, "deadline_days": 10, "is_required": False,
        "title": "Complete HRIS system training",
        "description": "Finish self-paced training modules for the HR information system.",
    },
    # Product Onboarding
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000008"),
        "template_id": TMPL_PROD_ID, "order": 1, "deadline_days": 2, "is_required": True,
        "title": "Meet the product team",
        "description": "Schedule 1:1s with each product team member and your PM lead.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000009"),
        "template_id": TMPL_PROD_ID, "order": 2, "deadline_days": 5, "is_required": True,
        "title": "Review product roadmap",
        "description": "Go through the current and upcoming quarter roadmap with your PM lead.",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0002-000000000010"),
        "template_id": TMPL_PROD_ID, "order": 3, "deadline_days": 14, "is_required": False,
        "title": "Shadow a customer call",
        "description": "Join a live customer demo or support call to understand user pain points.",
    },
]

# ─── Plans ────────────────────────────────────────────────────────────────────
#
# Plan 1 — employee@stepup.com (Engineering, in-progress)
#   Task 1 APPROVED, Task 2 RETURNED (returned by manager), Task 3 IN_PROGRESS, Task 4 NOT_STARTED + overdue
#   → Shows in task completion rates. Task 2 shows in bottlenecks.
#
# Plan 2 — alice@stepup.com (Engineering, completed)
#   All tasks APPROVED. start_date = 40 days ago.
#   → Shows in completion time report (Engineering, ~40 days avg).
#   → Shows in task completion rates (100% for Engineering Onboarding).
#
# Plan 3 — bob@stepup.com (Product, stuck)
#   Task 1 RETURNED, Task 2 RETURNED, Task 3 NOT_STARTED + overdue.
#   → Shows in bottlenecks report for Product Onboarding.

SEED_PLANS = [
    {
        "id": PLAN_EMP_ID,
        "user_id": EMPLOYEE_ID,
        "template_id": TMPL_ENG_ID,
        "manager_id": MANAGER_ID,
        "start_date": TODAY - timedelta(days=20),
        "tasks": [
            {
                "title": "Set up development environment",
                "description": "Install required tools: Git, Docker, VS Code, and configure local environment variables.",
                "deadline": TODAY - timedelta(days=19),
                "status": OnboardingPlanTaskStatus.APPROVED,
                "is_required": True, "order": 1,
            },
            {
                "title": "Complete security and compliance training",
                "description": "Finish the mandatory security awareness course on the learning portal.",
                "deadline": TODAY - timedelta(days=17),
                "status": OnboardingPlanTaskStatus.RETURNED,
                "is_required": True, "order": 2,
            },
            {
                "title": "Review architecture documentation",
                "description": "Read system design docs and schedule a walkthrough session with the tech lead.",
                "deadline": TODAY + timedelta(days=2),
                "status": OnboardingPlanTaskStatus.IN_PROGRESS,
                "is_required": True, "order": 3,
            },
            {
                "title": "Submit first pull request",
                "description": "Pick a starter task from the backlog, implement it, and open a PR for review.",
                "deadline": TODAY - timedelta(days=6),
                "status": OnboardingPlanTaskStatus.NOT_STARTED,
                "is_required": False, "order": 4,
            },
        ],
    },
    {
        "id": PLAN_ALICE_ID,
        "user_id": ALICE_ID,
        "template_id": TMPL_ENG_ID,
        "manager_id": MANAGER_ID,
        "start_date": TODAY - timedelta(days=40),
        "tasks": [
            {
                "title": "Set up development environment",
                "description": "Install required tools: Git, Docker, VS Code, and configure local environment variables.",
                "deadline": TODAY - timedelta(days=39),
                "status": OnboardingPlanTaskStatus.APPROVED,
                "is_required": True, "order": 1,
            },
            {
                "title": "Complete security and compliance training",
                "description": "Finish the mandatory security awareness course on the learning portal.",
                "deadline": TODAY - timedelta(days=37),
                "status": OnboardingPlanTaskStatus.APPROVED,
                "is_required": True, "order": 2,
            },
            {
                "title": "Review architecture documentation",
                "description": "Read system design docs and schedule a walkthrough session with the tech lead.",
                "deadline": TODAY - timedelta(days=35),
                "status": OnboardingPlanTaskStatus.APPROVED,
                "is_required": True, "order": 3,
            },
            {
                "title": "Submit first pull request",
                "description": "Pick a starter task from the backlog, implement it, and open a PR for review.",
                "deadline": TODAY - timedelta(days=26),
                "status": OnboardingPlanTaskStatus.APPROVED,
                "is_required": False, "order": 4,
            },
        ],
    },
    {
        "id": PLAN_BOB_ID,
        "user_id": BOB_ID,
        "template_id": TMPL_PROD_ID,
        "manager_id": MANAGER2_ID,
        "start_date": TODAY - timedelta(days=15),
        "tasks": [
            {
                "title": "Meet the product team",
                "description": "Schedule 1:1s with each product team member and your PM lead.",
                "deadline": TODAY - timedelta(days=13),
                "status": OnboardingPlanTaskStatus.RETURNED,
                "is_required": True, "order": 1,
            },
            {
                "title": "Review product roadmap",
                "description": "Go through the current and upcoming quarter roadmap with your PM lead.",
                "deadline": TODAY - timedelta(days=10),
                "status": OnboardingPlanTaskStatus.RETURNED,
                "is_required": True, "order": 2,
            },
            {
                "title": "Shadow a customer call",
                "description": "Join a live customer demo or support call to understand user pain points.",
                "deadline": TODAY - timedelta(days=1),
                "status": OnboardingPlanTaskStatus.NOT_STARTED,
                "is_required": False, "order": 3,
            },
        ],
    },
]

# ─── Audit Logs ───────────────────────────────────────────────────────────────

SEED_AUDIT_LOGS = [
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000001"),
        "actor_id": ADMIN_ID, "action": "user.invited",
        "entity_type": "invitation", "entity_id": uuid.UUID("00000000-0000-0000-0088-000000000001"),
        "detail": "alice@stepup.com invited as employee",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000002"),
        "actor_id": ADMIN_ID, "action": "user.invited",
        "entity_type": "invitation", "entity_id": uuid.UUID("00000000-0000-0000-0088-000000000002"),
        "detail": "bob@stepup.com invited as employee",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000003"),
        "actor_id": ALICE_ID, "action": "user.registered",
        "entity_type": "user", "entity_id": ALICE_ID,
        "detail": "Alice Chen completed registration",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000004"),
        "actor_id": BOB_ID, "action": "user.registered",
        "entity_type": "user", "entity_id": BOB_ID,
        "detail": "Bob Marley completed registration",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000005"),
        "actor_id": ADMIN_ID, "action": "plan.created",
        "entity_type": "onboarding_plan", "entity_id": PLAN_EMP_ID,
        "detail": "Plan created for employee@stepup.com",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000006"),
        "actor_id": ADMIN_ID, "action": "plan.created",
        "entity_type": "onboarding_plan", "entity_id": PLAN_ALICE_ID,
        "detail": "Plan created for alice@stepup.com",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000007"),
        "actor_id": ADMIN_ID, "action": "plan.created",
        "entity_type": "onboarding_plan", "entity_id": PLAN_BOB_ID,
        "detail": "Plan created for bob@stepup.com",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000008"),
        "actor_id": ALICE_ID, "action": "task.started",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000001"),
        "detail": "Set up development environment",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000009"),
        "actor_id": ALICE_ID, "action": "task.completed",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000001"),
        "detail": "Set up development environment",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000010"),
        "actor_id": MANAGER_ID, "action": "task.approved",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000001"),
        "detail": "Set up development environment",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000011"),
        "actor_id": EMPLOYEE_ID, "action": "task.started",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000002"),
        "detail": "Complete security and compliance training",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000012"),
        "actor_id": EMPLOYEE_ID, "action": "task.completed",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000002"),
        "detail": "Complete security and compliance training",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000013"),
        "actor_id": MANAGER_ID, "action": "task.returned",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000002"),
        "detail": "Complete security and compliance training — certificate screenshot missing",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000014"),
        "actor_id": BOB_ID, "action": "task.started",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000003"),
        "detail": "Meet the product team",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000015"),
        "actor_id": BOB_ID, "action": "task.completed",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000003"),
        "detail": "Meet the product team",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000016"),
        "actor_id": MANAGER2_ID, "action": "task.returned",
        "entity_type": "onboarding_plan_task", "entity_id": uuid.UUID("00000000-0000-0000-0077-000000000003"),
        "detail": "Meet the product team — needs documented meeting notes",
    },
    {
        "id": uuid.UUID("00000000-0000-0000-0099-000000000017"),
        "actor_id": ADMIN_ID, "action": "user.updated",
        "entity_type": "user", "entity_id": EMPLOYEE_ID,
        "detail": "Department updated",
    },
]


# ─── Seed helpers ─────────────────────────────────────────────────────────────

async def seed_departments(session: AsyncSession) -> None:
    for d in SEED_DEPARTMENTS:
        exists = (await session.execute(select(Department).where(Department.id == d["id"]))).scalar_one_or_none()
        if exists:
            print(f"  skip dept: {d['name']}")
            continue
        session.add(Department(id=d["id"], name=d["name"]))
        print(f"  + dept: {d['name']}")
    await session.commit()


async def seed_users(session: AsyncSession) -> None:
    for u in SEED_USERS:
        exists = (await session.execute(select(User).where(User.email == u["email"]))).scalar_one_or_none()
        if exists:
            print(f"  skip user: {u['email']}")
            continue
        session.add(User(
            id=u["id"],
            email=u["email"],
            password_hash=pwd_context.hash(u["password"]),
            first_name=u["first_name"],
            last_name=u["last_name"],
            role=u["role"],
            department_id=u["department_id"],
        ))
        print(f"  + user: {u['email']} / {u['password']}")
    await session.commit()


async def seed_templates(session: AsyncSession) -> None:
    for t in SEED_TEMPLATES:
        exists = (await session.execute(select(OnboardingTemplate).where(OnboardingTemplate.id == t["id"]))).scalar_one_or_none()
        if exists:
            print(f"  skip template: {t['name']}")
            continue
        session.add(OnboardingTemplate(id=t["id"], name=t["name"], department_id=t["department_id"], is_active=t["is_active"]))
        print(f"  + template: {t['name']}")
    await session.commit()


async def seed_template_tasks(session: AsyncSession) -> None:
    for t in SEED_TEMPLATE_TASKS:
        exists = (await session.execute(select(TemplateTask).where(TemplateTask.id == t["id"]))).scalar_one_or_none()
        if exists:
            print(f"  skip template task: {t['title']}")
            continue
        session.add(TemplateTask(
            id=t["id"],
            template_id=t["template_id"],
            title=t["title"],
            description=t["description"],
            order=t["order"],
            deadline_days=t["deadline_days"],
            is_required=t["is_required"],
        ))
        print(f"  + template task: {t['title']}")
    await session.commit()


async def seed_plans(session: AsyncSession) -> None:
    for p in SEED_PLANS:
        exists = (await session.execute(select(OnboardingPlan).where(OnboardingPlan.id == p["id"]))).scalar_one_or_none()
        if exists:
            print(f"  skip plan: {p['id']}")
            continue
        plan = OnboardingPlan(
            id=p["id"],
            user_id=p["user_id"],
            template_id=p["template_id"],
            manager_id=p["manager_id"],
            start_date=p["start_date"],
            is_active=True,
        )
        session.add(plan)
        await session.flush()

        for t in p["tasks"]:
            session.add(OnboardingPlanTask(
                plan_id=plan.id,
                title=t["title"],
                description=t["description"],
                deadline=t["deadline"],
                status=t["status"],
                is_required=t["is_required"],
                order=t["order"],
            ))
            print(f"  + plan task: {t['title']} ({t['status'].value})")

        await session.commit()
        print(f"  + plan: {p['id']}")


async def seed_audit_logs(session: AsyncSession) -> None:
    for a in SEED_AUDIT_LOGS:
        exists = (await session.execute(select(AuditLog).where(AuditLog.id == a["id"]))).scalar_one_or_none()
        if exists:
            print(f"  skip audit: {a['action']}")
            continue
        session.add(AuditLog(
            id=a["id"],
            actor_id=a["actor_id"],
            action=a["action"],
            entity_type=a["entity_type"],
            entity_id=a["entity_id"],
            detail=a["detail"],
        ))
        print(f"  + audit: {a['action']} — {a['detail']}")
    await session.commit()


# ─── Main ─────────────────────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("\n[Departments]")
        await seed_departments(session)

        print("\n[Users]")
        await seed_users(session)

        print("\n[Templates]")
        await seed_templates(session)

        print("\n[Template Tasks]")
        await seed_template_tasks(session)

        print("\n[Plans]")
        await seed_plans(session)

        print("\n[Audit Logs]")
        await seed_audit_logs(session)

    await engine.dispose()
    print("\nSeed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
