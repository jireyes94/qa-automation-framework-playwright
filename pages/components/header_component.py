from playwright.sync_api import Locator, Page


class HeaderComponent:
    def __init__(self, page: Page) -> None:
        self._page = page

    def logged_in_as(self, username: str) -> Locator:
        return self._page.get_by_text(
            f"Logged in as {username}"
        )