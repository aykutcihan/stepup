from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient

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
    dept = Department(name="Workflow Test Department")
    db_session.add(dept)
    await db_session.flush()
    return dept


@pytest.fixture
async def employee_user(db_session):
    user = User(
        email="employee_workflow_test@test.com",
        role=UserRole.EMPLOYEE,
        first_name="Employee",
        last_name="Workflow",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def manager_user(db_session):
    user = User(
        email="manager_workflow_test@test.com",
        role=UserRole.MANAGER,
        first_name="Manager",
        last_name="Workflow",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def plan_with_task(db_session, department, employee_user, manager_user):
    template = OnboardingTemplate(
        name="Workflow Template",
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
        title="Workflow Task",
        deadline=date(2026, 6, 8),
        status=OnboardingPlanTaskStatus.NOT_STARTED,
        is_required=True,
        order=1,
    )
    db_session.add(task)
    await db_session.flush()

    return plan, task


@pytest.fixture
async def employee_client(db_session, employee_user):
    async def override_get_db():
        yield db_session

    async def override_get_current_user():
        await db_session.refresh(employee_user)
        return employee_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class TestGetMyPlan:

    async def test_returns_200_with_tasks(self, employee_client, plan_with_task):
        plan, task = plan_with_task

        response = await employee_client.get("/api/v1/plans/me")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(plan.id)
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["status"] == "not_started"

    async def test_returns_404_when_no_active_plan(self, employee_client):
        response = await employee_client.get("/api/v1/plans/me")

        assert response.status_code == 404
        assert response.json()["error_code"] == "PLAN_NOT_FOUND"


class TestStartTask:

    async def test_returns_200_with_in_progress_status(self, employee_client, plan_with_task):
        _, task = plan_with_task

        response = await employee_client.patch(f"/api/v1/tasks/{task.id}/start")

        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    async def test_returns_400_for_invalid_transition_when_cancelled(
        self, employee_client, db_session, plan_with_task
    ):
        _, task = plan_with_task
        task.status = OnboardingPlanTaskStatus.CANCELLED
        await db_session.flush()

        response = await employee_client.patch(f"/api/v1/tasks/{task.id}/start")

        assert response.status_code == 400
        assert response.json()["error_code"] == "INVALID_TASK_TRANSITION"


class TestCompleteTask:

    async def test_returns_200_with_completed_status(
        self, employee_client, db_session, plan_with_task
    ):
        _, task = plan_with_task
        task.status = OnboardingPlanTaskStatus.IN_PROGRESS
        await db_session.flush()

        response = await employee_client.patch(f"/api/v1/tasks/{task.id}/complete")

        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    async def test_returns_400_when_not_started(self, employee_client, plan_with_task):
        _, task = plan_with_task

        response = await employee_client.patch(f"/api/v1/tasks/{task.id}/complete")

        assert response.status_code == 400
        assert response.json()["error_code"] == "INVALID_TASK_TRANSITION"
