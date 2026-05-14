import pytest
from datetime import date, timedelta

from app.enums.onboarding_plan_task_status import OnboardingPlanTaskStatus
from app.enums.user_role import UserRole
from app.models.department import Department
from app.models.onboarding_plan import OnboardingPlan
from app.models.onboarding_plan_task import OnboardingPlanTask
from app.models.onboarding_template import OnboardingTemplate
from app.models.user import User

pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture
async def department(db_session):
    dept = Department(name="Engineering")
    db_session.add(dept)
    await db_session.flush()
    return dept


@pytest.fixture
async def template(db_session, department):
    tmpl = OnboardingTemplate(
        name="Dev Onboarding",
        department_id=department.id,
        is_active=True,
    )
    db_session.add(tmpl)
    await db_session.flush()
    return tmpl


@pytest.fixture
async def employee(db_session, department):
    user = User(
        email="report_employee@test.com",
        role=UserRole.EMPLOYEE,
        first_name="Report",
        last_name="Employee",
        password_hash="placeholder",
        is_active=True,
        department_id=department.id,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def manager(db_session):
    user = User(
        email="report_manager@test.com",
        role=UserRole.MANAGER,
        first_name="Report",
        last_name="Manager",
        password_hash="placeholder",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture
async def approved_plan(db_session, employee, manager, template):
    plan = OnboardingPlan(
        user_id=employee.id,
        manager_id=manager.id,
        template_id=template.id,
        start_date=date.today() - timedelta(days=10),
        is_active=True,
    )
    db_session.add(plan)
    await db_session.flush()

    task = OnboardingPlanTask(
        plan_id=plan.id,
        title="Read Docs",
        deadline=date.today() + timedelta(days=7),
        status=OnboardingPlanTaskStatus.APPROVED,
        is_required=True,
        order=1,
    )
    db_session.add(task)
    await db_session.flush()
    return plan


@pytest.fixture
async def plan_with_returned_task(db_session, employee, manager, template):
    plan = OnboardingPlan(
        user_id=employee.id,
        manager_id=manager.id,
        template_id=template.id,
        start_date=date.today() - timedelta(days=5),
        is_active=True,
    )
    db_session.add(plan)
    await db_session.flush()

    task = OnboardingPlanTask(
        plan_id=plan.id,
        title="Write Tests",
        deadline=date.today() - timedelta(days=1),
        status=OnboardingPlanTaskStatus.RETURNED,
        is_required=True,
        order=1,
    )
    db_session.add(task)
    await db_session.flush()
    return plan


class TestCompletionTimeEndpoint:

    async def test_returns_department_rows(self, authenticated_client, approved_plan):
        resp = await authenticated_client.get("/api/v1/reports/completion-time")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert any(row["department_name"] == "Engineering" for row in data)

    async def test_returns_csv(self, authenticated_client, approved_plan):
        resp = await authenticated_client.get("/api/v1/reports/completion-time?format=csv")
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert "department_name" in resp.text

    async def test_date_filter_excludes_old_plans(self, authenticated_client, approved_plan):
        future = (date.today() + timedelta(days=30)).isoformat()
        resp = await authenticated_client.get(f"/api/v1/reports/completion-time?start_date={future}")
        assert resp.status_code == 200
        data = resp.json()
        assert not any(row["department_name"] == "Engineering" for row in data)


class TestTaskCompletionRatesEndpoint:

    async def test_returns_template_rows(self, authenticated_client, approved_plan):
        resp = await authenticated_client.get("/api/v1/reports/task-completion-rates")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert any(row["template_name"] == "Dev Onboarding" for row in data)

    async def test_completion_rate_calculation(self, authenticated_client, approved_plan):
        resp = await authenticated_client.get("/api/v1/reports/task-completion-rates")
        row = next(r for r in resp.json() if r["template_name"] == "Dev Onboarding")
        assert row["total_tasks"] >= 1
        assert row["completion_rate"] > 0

    async def test_returns_csv(self, authenticated_client, approved_plan):
        resp = await authenticated_client.get("/api/v1/reports/task-completion-rates?format=csv")
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert "template_name" in resp.text


class TestBottlenecksEndpoint:

    async def test_returns_returned_tasks(self, authenticated_client, plan_with_returned_task):
        resp = await authenticated_client.get("/api/v1/reports/bottlenecks")
        assert resp.status_code == 200
        data = resp.json()
        assert any(row["task_title"] == "Write Tests" for row in data)

    async def test_returned_count_correct(self, authenticated_client, plan_with_returned_task):
        resp = await authenticated_client.get("/api/v1/reports/bottlenecks")
        row = next(r for r in resp.json() if r["task_title"] == "Write Tests")
        assert row["returned_count"] >= 1

    async def test_returns_csv(self, authenticated_client, plan_with_returned_task):
        resp = await authenticated_client.get("/api/v1/reports/bottlenecks?format=csv")
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert "task_title" in resp.text


class TestReportsAuthorization:

    async def test_unauthenticated_rejected(self, client):
        resp = await client.get("/api/v1/reports/completion-time")
        assert resp.status_code == 401
