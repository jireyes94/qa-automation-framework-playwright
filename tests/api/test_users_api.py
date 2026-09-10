import allure
import pytest

from api.users_client import UsersClient
from test_data.user_factory import build_user


# API-001
@allure.feature("Users API")
@allure.story("Create user")
@pytest.mark.api
def test_create_user_endpoint(users_client: UsersClient) -> None:
    user = build_user()

    try:
        response = users_client.create_user(user.to_payload())
        body = response.json()

        assert response.status == 200
        assert body["responseCode"] == 201
        assert body["message"] == "User created!"
    finally:
        users_client.delete_user(
            email=user.email,
            password=user.password,
        )


# API-002
@allure.feature("Users API")
@allure.story("Reject duplicate user")
@pytest.mark.api
def test_reject_duplicate_user(users_client: UsersClient) -> None:
    user = build_user()
    payload = user.to_payload()

    create_response = users_client.create_user(payload)
    create_body = create_response.json()

    assert create_response.status == 200
    assert create_body["responseCode"] == 201
    assert create_body["message"] == "User created!"

    try:
        duplicate_response = users_client.create_user(payload)
        duplicate_body = duplicate_response.json()

        assert duplicate_response.status == 200
        assert duplicate_body["responseCode"] == 400
        assert duplicate_body["message"] == "Email already exists!"
    finally:
        delete_response = users_client.delete_user(
            email=user.email,
            password=user.password,
        )
        delete_body = delete_response.json()

        assert delete_response.status == 200
        assert delete_body["responseCode"] == 200
        assert delete_body["message"] == "Account deleted!"


# API-003
@allure.feature("Users API")
@allure.story("Delete user")
@pytest.mark.api
def test_delete_user(users_client: UsersClient) -> None:
    user = build_user()

    create_response = users_client.create_user(user.to_payload())
    create_body = create_response.json()

    assert create_response.status == 200
    assert create_body["responseCode"] == 201
    assert create_body["message"] == "User created!"

    delete_response = users_client.delete_user(
        email=user.email,
        password=user.password,
    )
    delete_body = delete_response.json()

    assert delete_response.status == 200
    assert delete_body["responseCode"] == 200
    assert delete_body["message"] == "Account deleted!"
