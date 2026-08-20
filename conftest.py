from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api.users_client import UsersClient
from test_data.user_factory import UserData, build_user


@pytest.fixture
def api_request_context(
    playwright: Playwright,
) -> Iterator[APIRequestContext]:
    request_context = playwright.request.new_context(
        base_url="https://automationexercise.com/api/",
    )

    yield request_context

    request_context.dispose()


@pytest.fixture
def users_client(
    api_request_context: APIRequestContext,
) -> UsersClient:
    return UsersClient(api_request_context)


@pytest.fixture
def registered_user(
    users_client: UsersClient,
) -> Iterator[UserData]:
    user = build_user()

    create_response = users_client.create_user(user.to_payload())
    create_body = create_response.json()

    assert create_response.status == 200
    assert create_body["responseCode"] == 201
    assert create_body["message"] == "User created!"

    yield user

    delete_response = users_client.delete_user(
        email=user.email,
        password=user.password,
    )
    delete_body = delete_response.json()

    assert delete_response.status == 200
    assert delete_body["responseCode"] == 200
    assert delete_body["message"] == "Account deleted!"
