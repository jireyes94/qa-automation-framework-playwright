from playwright.sync_api import Locator, Page
from pages.components.cart_item import CartItem

class CartPage:
    def __init__(self, page: Page) -> None:
        self._page = page

    def open(self) -> None:
            self._page.goto("/view_cart")

    def item_by_name(self, product_name: str) -> CartItem:
        root = self._page.locator(
            f"tr:has(td.cart_description:has-text('{product_name}'))"
        )
        return CartItem(root)