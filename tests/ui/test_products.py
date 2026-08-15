import pytest 
from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage

#PROD-001
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
@pytest.mark.ui
def test_product_search_returns_expected_results(
    page: Page,
) -> None:
    product_name = "Blue Top"
    products_page = ProductsPage(page)

    products_page.open()
    products_page.search(product_name)

    expect(products_page.title).to_have_text("Searched Products")

    product_card = products_page.product_by_name(product_name)

    expect(product_card.name).to_have_text(product_name)

# PROD-003
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

# CART-001
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
    expect(cart_modal.message).to_have_text(
        "Your product has been added to cart."
    )

    cart_page = cart_modal.view_cart()
    cart_item = cart_page.item_by_name(expected_name)

    expect(cart_item.name).to_have_text(expected_name)
    expect(cart_item.price).to_have_text(expected_price)