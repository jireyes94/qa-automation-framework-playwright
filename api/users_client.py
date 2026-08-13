from playwright.sync_api import APIRequestContext, APIResponse


class UsersClient:
    def __init__(self, request_context: APIRequestContext) -> None:
        self._request_context = request_context

    def create_user(self, payload: dict[str, str]) -> APIResponse:
        return self._request_context.post(
            "createAccount",
            form=payload,
        )

    def delete_user(self, email: str, password: str) -> APIResponse:
        return self._request_context.delete(
            "deleteAccount",
            form={
                "email": email,
                "password": password,
            },
        )