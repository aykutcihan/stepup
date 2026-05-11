import pytest
from app.models.template_task import TemplateTask

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def create_department(client, name="Test Department"):
    response = await client.post("/api/v1/departments/", json={"name": name})
    return response.json()["id"]


async def create_template(client, department_id, name="Test Template"):
    response = await client.post(
        "/api/v1/templates/",
        json={"name": name, "department_id": department_id},
    )
    return response.json()


async def add_task(client, template_id, title="Test Task"):
    response = await client.post(
        f"/api/v1/templates/{template_id}/tasks",
        json={"title": title, "deadline_days": 3, "is_required": True},
    )
    return response.json()


class TestGetTasks:

    async def test_get_tasks_returns_200_with_list(self, authenticated_client):
        department_id = await create_department(authenticated_client, "GetTasks Dept")
        template = await create_template(authenticated_client, department_id, "GetTasks Template")
        await add_task(authenticated_client, template["id"], "Task A")

        response = await authenticated_client.get(
            f"/api/v1/templates/{template['id']}/tasks"
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == "Task A"

    async def test_get_tasks_returns_404_when_template_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.get(
            "/api/v1/templates/00000000-0000-0000-0000-000000000000/tasks"
        )

        assert response.status_code == 404


class TestPostTemplate:

    async def test_post_template_returns_201_when_request_is_valid(
        self, authenticated_client
    ):
        department_id = await create_department(authenticated_client, "Engineering")

        response = await authenticated_client.post(
            "/api/v1/templates/",
            json={"name": "Engineering Onboarding", "department_id": department_id},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Engineering Onboarding"
        assert data["department_id"] == department_id
        assert data["is_active"] is False

    async def test_post_template_returns_422_when_department_id_missing(
        self, authenticated_client
    ):
        response = await authenticated_client.post(
            "/api/v1/templates/",
            json={"name": "No Department Template"},
        )

        assert response.status_code == 422


class TestPostTask:

    async def test_post_task_returns_201_with_correct_order(self, authenticated_client):
        department_id = await create_department(authenticated_client, "PostTask Dept")
        template = await create_template(authenticated_client, department_id, "PostTask Template")

        await authenticated_client.post(
            f"/api/v1/templates/{template['id']}/tasks",
            json={"title": "First Task", "deadline_days": 1, "is_required": True},
        )
        response = await authenticated_client.post(
            f"/api/v1/templates/{template['id']}/tasks",
            json={"title": "Second Task", "deadline_days": 2, "is_required": False},
        )

        assert response.status_code == 201
        assert response.json()["order"] == 2
        assert response.json()["title"] == "Second Task"

    async def test_post_task_returns_404_when_template_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.post(
            "/api/v1/templates/00000000-0000-0000-0000-000000000000/tasks",
            json={"title": "Task", "deadline_days": 1, "is_required": True},
        )

        assert response.status_code == 404


class TestPatchTask:

    async def test_patch_task_returns_200_when_updated(self, authenticated_client):
        department_id = await create_department(authenticated_client, "PatchTask Dept")
        template = await create_template(authenticated_client, department_id, "PatchTask Template")
        task = await add_task(authenticated_client, template["id"], "Original Title")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/tasks/{task['id']}",
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    async def test_patch_task_returns_404_when_not_found(self, authenticated_client):
        department_id = await create_department(authenticated_client, "PatchTask404 Dept")
        template = await create_template(authenticated_client, department_id, "PatchTask404 Template")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/tasks/00000000-0000-0000-0000-000000000000",
            json={"title": "Anything"},
        )

        assert response.status_code == 404


class TestDeleteTask:

    async def test_delete_task_returns_204(self, authenticated_client):
        department_id = await create_department(authenticated_client, "DeleteTask Dept")
        template = await create_template(authenticated_client, department_id, "DeleteTask Template")
        task = await add_task(authenticated_client, template["id"], "To Delete")

        response = await authenticated_client.delete(
            f"/api/v1/templates/{template['id']}/tasks/{task['id']}"
        )

        assert response.status_code == 204

    async def test_delete_task_does_not_appear_in_list(self, authenticated_client):
        department_id = await create_department(authenticated_client, "DeleteCheck Dept")
        template = await create_template(authenticated_client, department_id, "DeleteCheck Template")
        task = await add_task(authenticated_client, template["id"], "To Delete Check")

        await authenticated_client.delete(
            f"/api/v1/templates/{template['id']}/tasks/{task['id']}"
        )

        response = await authenticated_client.get(
            f"/api/v1/templates/{template['id']}/tasks"
        )
        assert all(t["id"] != task["id"] for t in response.json())


class TestReorderTask:

    async def test_reorder_task_returns_200_with_new_order(self, authenticated_client):
        department_id = await create_department(authenticated_client, "Reorder Dept")
        template = await create_template(authenticated_client, department_id, "Reorder Template")
        await add_task(authenticated_client, template["id"], "Task 1")
        task_2 = await add_task(authenticated_client, template["id"], "Task 2")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/tasks/{task_2['id']}/reorder",
            json={"new_order": 1},
        )

        assert response.status_code == 200
        assert response.json()["order"] == 1

    async def test_reorder_task_returns_400_when_order_invalid(
        self, authenticated_client
    ):
        department_id = await create_department(authenticated_client, "ReorderInvalid Dept")
        template = await create_template(authenticated_client, department_id, "ReorderInvalid Template")
        task = await add_task(authenticated_client, template["id"], "Only Task")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/tasks/{task['id']}/reorder",
            json={"new_order": 99},
        )

        assert response.status_code == 400


class TestGetTemplates:

    async def test_get_templates_returns_200_with_list(self, authenticated_client):
        department_id = await create_department(authenticated_client, "Marketing")
        await create_template(authenticated_client, department_id, "Marketing Onboarding")

        response = await authenticated_client.get("/api/v1/templates/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_templates_filters_by_is_active(self, authenticated_client):
        department_id = await create_department(authenticated_client, "Finance")
        await create_template(authenticated_client, department_id, "Finance Onboarding")

        response = await authenticated_client.get(
            "/api/v1/templates/", params={"is_active": False}
        )

        assert response.status_code == 200
        assert all(t["is_active"] is False for t in response.json())


class TestPatchTemplate:

    async def test_patch_template_returns_200_when_name_updated(
        self, authenticated_client
    ):
        department_id = await create_department(authenticated_client, "Legal")
        template = await create_template(authenticated_client, department_id, "Legal Onboarding")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}",
            json={"name": "Legal Onboarding Updated"},
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Legal Onboarding Updated"

    async def test_patch_template_returns_404_when_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.patch(
            "/api/v1/templates/00000000-0000-0000-0000-000000000000",
            json={"name": "Anything"},
        )

        assert response.status_code == 404


class TestActivateTemplate:

    async def test_activate_returns_200_and_deactivates_previous(
        self, authenticated_client, db_session
    ):
        department_id = await create_department(authenticated_client, "Sales")

        first = await create_template(authenticated_client, department_id, "Sales v1")
        second = await create_template(authenticated_client, department_id, "Sales v2")

        task = TemplateTask(
            template_id=first["id"],
            title="Sign contract",
            order=1,
            deadline_days=1,
            is_required=True,
        )
        db_session.add(task)
        await db_session.flush()

        task2 = TemplateTask(
            template_id=second["id"],
            title="Setup laptop",
            order=1,
            deadline_days=3,
            is_required=True,
        )
        db_session.add(task2)
        await db_session.flush()

        await authenticated_client.patch(f"/api/v1/templates/{first['id']}/activate")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{second['id']}/activate"
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is True

        first_response = await authenticated_client.get("/api/v1/templates/")
        first_data = next(t for t in first_response.json() if t["id"] == first["id"])
        assert first_data["is_active"] is False

    async def test_activate_returns_400_when_no_tasks(self, authenticated_client):
        department_id = await create_department(authenticated_client, "Ops")
        template = await create_template(authenticated_client, department_id, "Ops Onboarding")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/activate"
        )

        assert response.status_code == 400


class TestDeactivateTemplate:

    async def test_deactivate_returns_200(self, authenticated_client, db_session):
        department_id = await create_department(authenticated_client, "Support")
        template = await create_template(
            authenticated_client, department_id, "Support Onboarding"
        )

        task = TemplateTask(
            template_id=template["id"],
            title="Read handbook",
            order=1,
            deadline_days=2,
            is_required=True,
        )
        db_session.add(task)
        await db_session.flush()

        await authenticated_client.patch(f"/api/v1/templates/{template['id']}/activate")

        response = await authenticated_client.patch(
            f"/api/v1/templates/{template['id']}/deactivate"
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is False


class TestCloneTemplate:

    async def test_clone_returns_201_with_inactive_copy(
        self, authenticated_client, db_session
    ):
        department_id = await create_department(authenticated_client, "Product")
        template = await create_template(
            authenticated_client, department_id, "Product Onboarding"
        )

        task = TemplateTask(
            template_id=template["id"],
            title="Meet the team",
            order=1,
            deadline_days=2,
            is_required=False,
        )
        db_session.add(task)
        await db_session.flush()

        response = await authenticated_client.post(
            f"/api/v1/templates/{template['id']}/clone"
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Product Onboarding (copy)"
        assert data["is_active"] is False
        assert data["department_id"] == department_id

    async def test_clone_returns_404_when_template_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.post(
            "/api/v1/templates/00000000-0000-0000-0000-000000000000/clone"
        )

        assert response.status_code == 404
