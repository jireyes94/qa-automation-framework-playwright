from playwright.sync_api import Page


class CategoryComponent:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._root = page.locator("#accordian")

    def select(self, group: str, category: str) -> None:
        group_link = self._root.get_by_role(
            "link",
            name=group,
        )
        group_link.click()

        category_panel = self._page.locator(f"#{group}")

        category_link = category_panel.get_by_role(
            "link",
            name=category,
        )
        category_link.click()
