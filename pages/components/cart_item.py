from playwright.sync_api import Locator


class CartItem:
    def __init__(self, root: Locator) -> None:
        self._root = root

        self._name = root.locator("td.cart_description > h4 > a")
        self._price = root.locator("td.cart_price > p")

    @property
    def name(self) -> Locator:
        return self._name

    @property
    def price(self) -> Locator:
        return self._price
