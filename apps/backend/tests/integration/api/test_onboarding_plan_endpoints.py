
import pytest

from app.enums.user_role import UserRole
from app.models.department import Department
from app.models.onboarding_template import OnboardingTemplate
from app.models.template_task import TemplateTask
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
async def department(db_session):
    dept = Department(name="Test Department")
    db_session.add(dept)
    await db_session.flush()
    return dept


@pytest.fixture
async def active_template(db_session, department):
    template = OnboardingTemplate(
        name="Test Template",
        department_id=department.id,
        is_active=True,
    )
    db_session.add(template)
    await db_session.flush()

    task = TemplateTask(
        template_id=template.id,
        title="First Task",
        order=1,
        deadline_days=7,
        is_required=True,
    )
    db_session.add(task)
    await db_session.flush()
    return template


@pytest.fixture
async def inactive_template(db_session, department):
    template = OnboardingTemplate(
        name="Inactive Template",
        department_id=department.id,
        is_active=False,
    )
    db_session.add(template)
    await db_session.flush()
    return template


@pytest.fixture
async def employee_user(db_session):
    user = User(
        email="employee_plan_test@test.com",
        role=UserRole.EMPLOYEE,
        first_name="Employee",
        last_name="Test",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def manager_user(db_session):
    user = User(
        email="manager_plan_test@test.com",
        role=UserRole.MANAGER,
        first_name="Manager",
        last_name="Test",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


class TestCreatePlan:

    async def test_create_plan_returns_201_with_tasks(
        self, authenticated_client, active_template, employee_user, manager_user
    ):
        response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == str(employee_user.id)
        assert data["is_active"] is True
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["deadline"] == "2026-06-08"

    async def test_create_plan_returns_400_when_employee_already_has_active_plan(
        self, authenticated_client, active_template, employee_user, manager_user
    ):
        await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-07-01",
            },
        )

        response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-08-01",
            },
        )

        assert response.status_code == 400
        assert response.json()["error_code"] == "EMPLOYEE_ALREADY_HAS_ACTIVE_PLAN"

    async def test_create_plan_returns_400_when_template_is_not_active(
        self, authenticated_client, inactive_template, employee_user, manager_user
    ):
        response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(inactive_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )

        assert response.status_code == 400
        assert response.json()["error_code"] == "TEMPLATE_NOT_ACTIVE"


class TestGetPlan:

    async def test_get_plan_returns_200(
        self, authenticated_client, active_template, employee_user, manager_user
    ):
        create_response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )
        plan_id = create_response.json()["id"]

        response = await authenticated_client.get(f"/api/v1/plans/{plan_id}")

        assert response.status_code == 200
        assert response.json()["id"] == plan_id

    async def test_get_plan_returns_404_when_not_found(self, authenticated_client):
        response = await authenticated_client.get(
            "/api/v1/plans/00000000-0000-0000-0000-000000000000"
        )

        assert response.status_code == 404


class TestUpdatePlan:

    async def test_patch_plan_returns_200_when_manager_changed(
        self, authenticated_client, active_template, employee_user, manager_user, db_session
    ):
        create_response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )
        plan_id = create_response.json()["id"]

        new_manager = User(
            email="new_manager_plan_test@test.com",
            role=UserRole.MANAGER,
            first_name="New",
            last_name="Manager",
            password_hash="placeholder",
            is_active=True,
        )
        db_session.add(new_manager)
        await db_session.flush()

        response = await authenticated_client.patch(
            f"/api/v1/plans/{plan_id}",
            json={"manager_id": str(new_manager.id)},
        )

        assert response.status_code == 200
        assert response.json()["manager_id"] == str(new_manager.id)

    async def test_patch_plan_returns_404_when_not_found(self, authenticated_client, manager_user):
        response = await authenticated_client.patch(
            "/api/v1/plans/00000000-0000-0000-0000-000000000000",
            json={"manager_id": str(manager_user.id)},
        )

        assert response.status_code == 404


class TestCancelTask:

    async def test_cancel_task_returns_200_with_cancelled_status(
        self, authenticated_client, active_template, employee_user, manager_user
    ):
        create_response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )
        plan_data = create_response.json()
        plan_id = plan_data["id"]
        task_id = plan_data["tasks"][0]["id"]

        response = await authenticated_client.patch(
            f"/api/v1/plans/{plan_id}/tasks/{task_id}/cancel"
        )

        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

    async def test_cancel_task_returns_400_when_already_cancelled(
        self, authenticated_client, active_template, employee_user, manager_user
    ):
        create_response = await authenticated_client.post(
            "/api/v1/plans/",
            json={
                "user_id": str(employee_user.id),
                "template_id": str(active_template.id),
                "manager_id": str(manager_user.id),
                "start_date": "2026-06-01",
            },
        )
        plan_data = create_response.json()
        plan_id = plan_data["id"]
        task_id = plan_data["tasks"][0]["id"]

        await authenticated_client.patch(f"/api/v1/plans/{plan_id}/tasks/{task_id}/cancel")
        response = await authenticated_client.patch(
            f"/api/v1/plans/{plan_id}/tasks/{task_id}/cancel"
        )

        assert response.status_code == 400
        assert response.json()["error_code"] == "TASK_ALREADY_TERMINAL"
