import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


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
