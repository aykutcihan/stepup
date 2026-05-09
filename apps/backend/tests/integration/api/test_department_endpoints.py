import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestPatchDepartment:

    async def test_patch_department_returns_200_when_name_is_updated(
        self, authenticated_client
    ):
        create_response = await authenticated_client.post(
            "/api/v1/departments/", json={"name": "OldName"}
        )
        department_id = create_response.json()["id"]

        response = await authenticated_client.patch(
            f"/api/v1/departments/{department_id}",
            json={"name": "NewName"},
        )

        assert response.status_code == 200
        assert response.json()["name"] == "NewName"

    async def test_patch_department_returns_404_when_department_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.patch(
            "/api/v1/departments/00000000-0000-0000-0000-000000000000",
            json={"name": "Anything"},
        )

        assert response.status_code == 404

    async def test_patch_department_returns_400_when_name_already_exists(
        self, authenticated_client
    ):
        await authenticated_client.post("/api/v1/departments/", json={"name": "Existing"})
        create_response = await authenticated_client.post(
            "/api/v1/departments/", json={"name": "ToRename"}
        )
        department_id = create_response.json()["id"]

        response = await authenticated_client.patch(
            f"/api/v1/departments/{department_id}",
            json={"name": "Existing"},
        )

        assert response.status_code == 400


class TestGetDepartments:

    async def test_get_departments_returns_200_with_list(
        self, authenticated_client
    ):
        await authenticated_client.post("/api/v1/departments/", json={"name": "Finance"})

        response = await authenticated_client.get("/api/v1/departments/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(d["name"] == "Finance" for d in data)


class TestPostDepartment:

    async def test_post_department_returns_201_when_request_is_valid(
        self, authenticated_client
    ):
        response = await authenticated_client.post(
            "/api/v1/departments/",
            json={"name": "Engineering"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Engineering"
        assert data["is_active"] is True
        assert "id" in data

    async def test_post_department_returns_400_when_name_already_exists(
        self, authenticated_client
    ):
        await authenticated_client.post(
            "/api/v1/departments/",
            json={"name": "HR"},
        )

        response = await authenticated_client.post(
            "/api/v1/departments/",
            json={"name": "HR"},
        )

        assert response.status_code == 400
