from playwright.sync_api import Locator, Page

from pages.product_details_page import ProductDetailsPage
from pages.components.cart_modal import CartModal


class ProductCard:
    def __init__(self, page: Page, root: Locator) -> None:
        self._page = page
        self._root = root

        self._info = root.locator(".productinfo")
        self._overlay = root.locator(".product-overlay")

        self._name = self._info.locator("p")
        self._price = self._info.locator("h2")

    @property
    def container(self) -> Locator:
        return self._root

    @property
    def name(self) -> Locator:
        return self._name

    @property
    def price(self) -> Locator:
        return self._price

    def view_details(self) -> ProductDetailsPage:
        self._root.get_by_role(
            "link",
            name="View Product",
        ).click()
        return ProductDetailsPage(self._page)

    def add_to_cart(self) -> CartModal:
        self._root.hover()
    
        add_to_cart = self._overlay.locator(".add-to-cart")
    
        add_to_cart.click()
    
        return CartModal(self._page)