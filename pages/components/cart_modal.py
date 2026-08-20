from playwright.sync_api import Locator, Page

from pages.cart_page import CartPage


class CartModal:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._root = page.locator("#cartModal")

        self._title = self._root.locator("div.modal-header > h4")
        self._message = self._root.get_by_text(
            "Your product has been added to cart.",
            exact=True,
        )

    @property
    def title(self) -> Locator:
        return self._title

    @property
    def message(self) -> Locator:
        return self._message

    def view_cart(self) -> CartPage:
        self._root.get_by_role(
            "link",
            name="View Cart",
        ).click()
        return CartPage(self._page)
