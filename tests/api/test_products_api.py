import allure
import pytest

from api.products_client import ProductsClient


# API-004
@allure.feature("Products API")
@allure.story("Get all products")
@pytest.mark.api
def test_get_all_products(products_client: ProductsClient) -> None:
    response = products_client.get_all_products()

    assert response.status == 200

    body = response.json()

    assert body["responseCode"] == 200

    products = body["products"]

    assert isinstance(products, list)
    assert len(products) > 0

    product_ids = [product["id"] for product in products]
    assert len(product_ids) == len(set(product_ids))

    expected_keys = {
        "id",
        "name",
        "price",
        "brand",
        "category",
    }

    for product in products:
        assert set(product.keys()) == expected_keys

    representative_product = products[0]

    assert isinstance(representative_product["id"], int)
    assert representative_product["name"]
    assert representative_product["price"]
    assert representative_product["brand"]

    category = representative_product["category"]

    assert "category" in category
    assert "usertype" in category
    assert "usertype" in category["usertype"]


# API-002
