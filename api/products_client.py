from playwright.sync_api import APIRequestContext, APIResponse


class ProductsClient:
    def __init__(self, request_context: APIRequestContext) -> None:
        self._request_context = request_context

    def get_all_products(self) -> APIResponse:
        return self._request_context.get("productsList")
