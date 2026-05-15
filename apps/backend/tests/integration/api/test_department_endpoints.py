import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestReactivateDepartment:

    async def test_reactivate_department_returns_200(self, authenticated_client):
        create_response = await authenticated_client.post(
            "/api/v1/departments/", json={"name": "ToReactivate"}
        )
        department_id = create_response.json()["id"]
        await authenticated_client.patch(f"/api/v1/departments/{department_id}/deactivate")

        response = await authenticated_client.patch(
            f"/api/v1/departments/{department_id}/reactivate"
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is True

    async def test_reactivate_department_returns_404_when_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.patch(
            "/api/v1/departments/00000000-0000-0000-0000-000000000000/reactivate"
        )

        assert response.status_code == 404


class TestDeactivateDepartment:

    async def test_deactivate_department_returns_200_when_no_active_users(
        self, authenticated_client
    ):
        create_response = await authenticated_client.post(
            "/api/v1/departments/", json={"name": "ToDeactivate"}
        )
        department_id = create_response.json()["id"]

        response = await authenticated_client.patch(
            f"/api/v1/departments/{department_id}/deactivate"
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is False

    async def test_deactivate_department_returns_404_when_not_found(
        self, authenticated_client
    ):
        response = await authenticated_client.patch(
            "/api/v1/departments/00000000-0000-0000-0000-000000000000/deactivate"
        )

        assert response.status_code == 404


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
        assert "items" in data
        assert any(d["name"] == "Finance" for d in data["items"])

    async def test_get_departments_returns_pagination_metadata(
        self, authenticated_client
    ):
        response = await authenticated_client.get("/api/v1/departments/?page=1&page_size=10")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert "total" in data
        assert data["has_prev"] is False

    async def test_get_departments_page_size_above_limit_returns_422(
        self, authenticated_client
    ):
        response = await authenticated_client.get("/api/v1/departments/?page_size=101")

        assert response.status_code == 422

    async def test_get_departments_page_zero_returns_422(
        self, authenticated_client
    ):
        response = await authenticated_client.get("/api/v1/departments/?page=0")

        assert response.status_code == 422


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
