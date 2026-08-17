from playwright.sync_api import Page


class BrandComponent:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._root = page.locator(".brands-name")

    def select(self, brand: str) -> None:
        brand_link = self._root.get_by_role(
            "link",
            name=brand,
        )
        brand_link.click()