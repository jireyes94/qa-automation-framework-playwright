import pytest
from playwright.sync_api import Page, expect
from test_data.user_factory import UserData
from pages.components.header_component import HeaderComponent
from pages.login_page import LoginPage

#AUTH-002
@pytest.mark.ui
def test_user_cannot_login_with_invalid_credentials(
    page: Page,
) -> None:
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(
        "invalid.user@example.com",
        "invalid-password",
    )

    expect(login_page.error_message).to_have_text(
        "Your email or password is incorrect!"
    )
    expect(page).to_have_url("/login")

#AUTH-001
@pytest.mark.ui
def test_user_can_login_with_valid_credentials(
    page: Page,
    registered_user: UserData,
) -> None:
    login_page = LoginPage(page)
    header = HeaderComponent(page)

    login_page.open()
    login_page.login(
        registered_user.email,
        registered_user.password,
    )

    expect(
        header.logged_in_as(registered_user.name)
    ).to_be_visible()