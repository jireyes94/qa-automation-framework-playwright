import pytest

from api.users_client import UsersClient
from test_data.user_factory import build_user


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