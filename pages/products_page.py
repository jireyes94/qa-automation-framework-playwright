from playwright.sync_api import Locator, Page
from pages.components.product_card import ProductCard
from pages.components.category_component import CategoryComponent
from pages.components.brand_component import BrandComponent


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._category = CategoryComponent(page)
        self._brand = BrandComponent(page)

    def open(self) -> None:
        self._page.goto("/products")

    @property
    def title(self) -> Locator:
        return self._page.locator("h2.title")

    @property
    def category(self) -> CategoryComponent:
        return self._category

    @property
    def brand(self) -> BrandComponent:
        return self._brand

    def product_by_id(self, product_id: str) -> ProductCard:
        product_card_locator = self._page.locator(
            f".product-image-wrapper:has([data-product-id='{product_id}'])"
        )

        return ProductCard(
            self._page,
            product_card_locator,
        )

    def search(self, query: str) -> None:
        search_input = self._page.locator("#search_product")
        search_button = self._page.locator("#submit_search")

        search_input.fill(query)
        search_button.click()

    def product_by_name(self, product_name: str) -> ProductCard:
        product_card_locator = self._page.locator(
            f".product-image-wrapper:has-text('{product_name}')"
        )

        return ProductCard(
            self._page,
            product_card_locator,
        )

    def product_cards(self) -> list[ProductCard]:
        cards = self._page.locator(".product-image-wrapper")
    
        return [
            ProductCard(self._page, cards.nth(index))
            for index in range(cards.count())
        ]