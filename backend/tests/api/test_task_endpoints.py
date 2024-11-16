import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.core.constants import TaskStatus
from main import app


pytest_plugins = ("pytest_asyncio",)
TEST_EMAIL = "test_tasks@test.com"
TEST_PASSWORD = "test"


@pytest.mark.asyncio
async def test_tasks():
    """Tests tasks endpoints"""
    client = TestClient(app)
    user_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}

    # Create user
    response = client.post(
        client.app.url_path_for("user_create"),
        json=user_data,
        headers={"Authorization": "Bearer test"},
    )

    # Create token
    response = client.post(
        client.app.url_path_for("auth_get_token"),
        json=user_data,
        headers={"Authorization": "Bearer test"},
    )
    token = response.json()["token"]

    task_data = {"title": "test", "description": "test"}
    # Create task
    response = client.post(
        client.app.url_path_for("task_create"),
        json=task_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Get tasks
    response = client.get(
        client.app.url_path_for("get_user_tasks"),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    task_response = response.json()["payload"]["tasks"][0]
    assert task_response["title"] == "test"
    assert task_response["description"] == "test"
    assert task_response["status"] == TaskStatus.TODO.value

    # Update task
    task_update_data = {
        "title": "test2",
        "description": "test2",
        "status": TaskStatus.IN_PROGRESS.value,
    }
    client.patch(
        client.app.url_path_for("task_update", task_id=task_response["task_id"]),
        json=task_update_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get tasks
    response = client.get(
        client.app.url_path_for("get_user_tasks"),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_200_OK
    task_response = response.json()["payload"]["tasks"][0]
    assert task_response["title"] == "test2"
    assert task_response["description"] == "test2"
    assert task_response["status"] == TaskStatus.IN_PROGRESS.value

    # Delete task
    response = client.delete(
        client.app.url_path_for("task_delete", task_id=task_response["task_id"]),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
