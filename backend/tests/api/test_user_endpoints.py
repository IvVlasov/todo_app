import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.api.v1.auth.services.jwt_token import create_access_token, decode_jwt
from backend.core.models.user import User
from main import app


pytest_plugins = ("pytest_asyncio",)
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "test"


@pytest.mark.asyncio
async def test_user():
    """Tests user endpoints"""
    client = TestClient(app)
    data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}

    # Test user creation
    response = client.post(
        client.app.url_path_for("user_create"),
        json=data,
        headers={"Authorization": "Bearer test"},
    )
    user_id = response.json()["payload"]["user_id"]
    assert response.status_code == status.HTTP_200_OK

    # Test token creation
    response = client.post(
        client.app.url_path_for("auth_get_token"),
        json=data,
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()

    # Test token encoding
    created_token = response.json()["token"]
    test_token = create_access_token(
        User(user_id=user_id, email=TEST_EMAIL, password=TEST_PASSWORD)
    )
    assert created_token == test_token

    # Test token decoding
    decoded_token = decode_jwt(created_token)
    assert decoded_token.user_id == user_id
    assert decoded_token.email == TEST_EMAIL
