from playwright.sync_api import Locator, Page


class ProductDetailsPage:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._product_information = page.locator(".product-information")

        self._name = self._product_information.locator("h2")
        self._category = self._product_information.locator("p:has-text('Category')")
        self._brand = self._product_information.locator("p:has-text('Brand')")
        self._price = self._product_information.locator("span > span")

    @property
    def name(self) -> Locator:
        return self._name

    @property
    def price(self) -> Locator:
        return self._price

    @property
    def category(self) -> Locator:
        return self._category

    @property
    def brand(self) -> Locator:
        return self._brand