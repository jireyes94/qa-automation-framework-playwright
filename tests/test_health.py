from playwright.sync_api import Page


def test_homepage_is_accessible(page: Page) -> None:
    page.goto("https://automationexercise.com")

    assert page.title()
