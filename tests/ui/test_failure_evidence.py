import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_failure_evidence_capture(page: Page) -> None:
    page.goto("/products")

    expect(page.locator("h2.title")).to_have_text(
        "THIS SHOULD FAIL"
    )