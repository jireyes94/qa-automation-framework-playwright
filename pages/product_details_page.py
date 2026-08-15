from playwright.sync_api import Locator, Page


class ProductDetailsPage:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._product_information = page.locator(".product-information")

        self._name = self._product_information.locator("h2")
        self._price = self._product_information.locator("span > span")

    @property
    def name(self) -> Locator:
        return self._name

    @property
    def price(self) -> Locator:
        return self._price