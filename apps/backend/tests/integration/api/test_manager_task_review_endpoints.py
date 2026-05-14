import pytest
from datetime import date
from httpx import AsyncClient, ASGITransport

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.enums.user_role import UserRole
from app.main import app
from app.models.department import Department
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.onboarding_template import OnboardingTemplate
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
async def department(db_session):
    dept = Department(name="Manager Review Department")
    db_session.add(dept)
    await db_session.flush()
    return dept


@pytest.fixture
async def employee_user(db_session):
    user = User(
        email="employee_mgr_review_test@test.com",
        role=UserRole.EMPLOYEE,
        first_name="John",
        last_name="Employee",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def manager_user(db_session):
    user = User(
        email="manager_mgr_review_test@test.com",
        role=UserRole.MANAGER,
        first_name="Jane",
        last_name="Manager",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def plan_with_completed_task(db_session, department, employee_user, manager_user):
    template = OnboardingTemplate(
        name="Manager Review Template",
        department_id=department.id,
        is_active=True,
    )
    db_session.add(template)
    await db_session.flush()

    plan = OnboardingPlan(
        user_id=employee_user.id,
        template_id=template.id,
        manager_id=manager_user.id,
        start_date=date(2026, 6, 1),
        is_active=True,
    )
    db_session.add(plan)
    await db_session.flush()

    task = OnboardingPlanTask(
        plan_id=plan.id,
        title="Review Task",
        deadline=date(2026, 6, 8),
        status=OnboardingPlanTaskStatus.COMPLETED,
        is_required=True,
        order=1,
    )
    db_session.add(task)
    await db_session.flush()

    return plan, task


@pytest.fixture
async def manager_client(db_session, manager_user):
    async def override_get_db():
        yield db_session

    async def override_get_current_user():
        await db_session.refresh(manager_user)
        return manager_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class TestGetPendingApprovals:

    async def test_returns_200_with_completed_tasks(
        self, manager_client, plan_with_completed_task
    ):
        response = await manager_client.get("/api/v1/manager/approvals")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Review Task"
        assert data[0]["employee_name"] == "John Employee"
        assert data[0]["status"] == "completed"

    async def test_returns_empty_list_when_no_completed_tasks(self, manager_client):
        response = await manager_client.get("/api/v1/manager/approvals")

        assert response.status_code == 200
        assert response.json() == []


class TestApproveTask:

    async def test_returns_200_with_approved_status(
        self, manager_client, plan_with_completed_task
    ):
        _, task = plan_with_completed_task

        response = await manager_client.patch(f"/api/v1/tasks/{task.id}/approve")

        assert response.status_code == 200
        assert response.json()["status"] == "approved"

    async def test_returns_400_when_task_not_completed(
        self, manager_client, db_session, plan_with_completed_task
    ):
        _, task = plan_with_completed_task
        task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        await db_session.flush()

        response = await manager_client.patch(f"/api/v1/tasks/{task.id}/approve")

        assert response.status_code == 400
        assert response.json()["error_code"] == "TASK_NOT_APPROVABLE"


class TestReturnTask:

    async def test_returns_200_with_in_progress_status(
        self, manager_client, plan_with_completed_task
    ):
        _, task = plan_with_completed_task

        response = await manager_client.patch(
            f"/api/v1/tasks/{task.id}/return",
            json={"content": "Please redo this task."},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    async def test_returns_400_when_content_missing(
        self, manager_client, plan_with_completed_task
    ):
        _, task = plan_with_completed_task

        response = await manager_client.patch(
            f"/api/v1/tasks/{task.id}/return",
            json={"content": "   "},
        )

        assert response.status_code == 400
        assert response.json()["error_code"] == "RETURN_COMMENT_REQUIRED"
