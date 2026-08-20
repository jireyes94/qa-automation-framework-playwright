import allure
import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage


# PROD-001
@allure.feature("Product Catalog")
@allure.story("Catalog")
@pytest.mark.ui
def test_product_catalog_displays_expected_product(
    page: Page,
) -> None:
    products_page = ProductsPage(page)

    products_page.open()
    product_card = products_page.product_by_id("1")

    expect(product_card.container).to_be_visible()
    expect(product_card.name).to_have_text("Blue Top")


# PROD-002
@allure.feature("Product Catalog")
@allure.story("Product Search")
@pytest.mark.ui
@pytest.mark.parametrize(
    "search_term",
    ["blue", "BLUE"],
)
def test_product_search_returns_expected_results(
    page: Page,
    search_term: str,
) -> None:
    products_page = ProductsPage(page)

    products_page.open()
    products_page.search(search_term)

    expect(products_page.title).to_have_text("Searched Products")

    results = products_page.product_cards()

    assert len(results) > 0, "Expected search to return at least one product"

    for product in results:
        product_name = product.name.inner_text()

        assert search_term.lower() in product_name.lower()


# PROD-003
@allure.feature("Product Catalog")
@allure.story("Product Details")
@pytest.mark.ui
def test_product_details_page_displays_expected_information(
    page: Page,
) -> None:
    products_page = ProductsPage(page)

    products_page.open()
    product_card = products_page.product_by_name("Blue Top")

    expected_name = product_card.name.inner_text()
    expected_price = product_card.price.inner_text()

    product_details_page = product_card.view_details()

    expect(product_details_page.name).to_have_text(expected_name)
    expect(product_details_page.price).to_have_text(expected_price)


# PROD-004
@allure.feature("Product Catalog")
@allure.story("Product Search")
@pytest.mark.ui
def test_product_search_with_no_matches_returns_no_results(
    page: Page,
) -> None:
    search_term = "zzzzzzzz"
    products_page = ProductsPage(page)

    products_page.open()
    products_page.search(search_term)

    expect(products_page.title).to_have_text("Searched Products")

    results = products_page.product_cards()
    assert not results, "Expected no products for an unmatched search"


# PROD-005
@allure.feature("Product Catalog")
@allure.story("Product Search")
@pytest.mark.ui
def test_empty_search_keeps_all_products_state(
    page: Page,
) -> None:
    products_page = ProductsPage(page)
    products_page.open()
    products_page.search("")

    expect(products_page.title).to_have_text("All Products")


# CART-001
@allure.feature("Shopping Cart")
@allure.story("Add Product")
@pytest.mark.ui
def test_add_product_to_cart_adds_product_to_cart(
    page: Page,
) -> None:
    products_page = ProductsPage(page)

    products_page.open()
    product_card = products_page.product_by_name("Blue Top")

    expected_name = product_card.name.inner_text()
    expected_price = product_card.price.inner_text()

    cart_modal = product_card.add_to_cart()

    expect(cart_modal.title).to_have_text("Added!")
    expect(cart_modal.message).to_have_text("Your product has been added to cart.")

    cart_page = cart_modal.view_cart()
    cart_item = cart_page.item_by_name(expected_name)

    expect(cart_item.name).to_have_text(expected_name)
    expect(cart_item.price).to_have_text(expected_price)


# CATEGORY-001
@allure.feature("Product Catalog")
@allure.story("Category Filtering")
@pytest.mark.ui
def test_select_category_displays_expected_products(
    page: Page,
) -> None:
    group = "Kids"
    category = "Dress"

    products_page = ProductsPage(page)

    products_page.open()
    products_page.category.select(group, category)

    expect(products_page.title).to_have_text(f"{group} - {category} Products")

    results = products_page.product_cards()
    assert results, "Expected at least one product in the selected category"


# CATEGORY-002
@allure.feature("Product Catalog")
@allure.story("Category Filtering")
@pytest.mark.ui
def test_category_result_matches_selected_category(
    page: Page,
) -> None:
    group = "Kids"
    category = "Dress"

    products_page = ProductsPage(page)

    products_page.open()
    products_page.category.select(group, category)

    results = products_page.product_cards()
    assert results, "Expected category to return at least one product"

    first_item = results[0]
    product_details_page = first_item.view_details()

    expect(product_details_page.category).to_have_text(
        f"Category: {group} > {category}"
    )


# BRAND-001
@allure.feature("Product Catalog")
@allure.story("Brand Filtering")
@pytest.mark.ui
def test_select_brand_displays_expected_products(
    page: Page,
) -> None:
    brand = "Polo"

    products_page = ProductsPage(page)

    products_page.open()
    products_page.brand.select(brand)

    expect(page).to_have_url(f"/brand_products/{brand}")
    expect(products_page.title).to_have_text(f"Brand - {brand} Products")

    results = products_page.product_cards()
    assert results, "Expected at least one product in the selected brand"


# BRAND-002
@allure.feature("Product Catalog")
@allure.story("Brand Filtering")
@pytest.mark.ui
def test_brand_result_matches_selected_brand(
    page: Page,
) -> None:
    brand = "Polo"

    products_page = ProductsPage(page)

    products_page.open()
    products_page.brand.select(brand)

    results = products_page.product_cards()
    assert results, "Expected brand to return at least one product"

    first_item = results[0]
    product_details_page = first_item.view_details()

    expect(product_details_page.brand).to_have_text(f"Brand: {brand}")
