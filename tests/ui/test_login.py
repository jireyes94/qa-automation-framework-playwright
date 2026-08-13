import pytest 
from playwright.sync_api import Page, expect
from test_data.user_factory import UserData

@pytest.mark.ui
def test_user_cannot_login_with_invalid_credentials(page: Page) -> None:
    page.goto("/login")

    email_input = page.locator("input[data-qa='login-email']") 
    password_input = page.locator("input[data-qa='login-password']")
    login_button = page.get_by_role("button", name="Login")

    email_input.fill("invalid.user@example.com")
    password_input.fill("invalid-password")
    login_button.click()

    error_message = page.get_by_text("Your email or password is incorrect!")

    expect(error_message).to_have_text("Your email or password is incorrect!")
    expect(page).to_have_url("/login")

@pytest.mark.ui
def test_user_can_login_with_valid_credentials(
    page: Page,
    registered_user: UserData,
) -> None:
    page.goto("/login")

    email_input = page.locator("input[data-qa='login-email']")
    password_input = page.locator("input[data-qa='login-password']")
    login_button = page.get_by_role("button", name="Login")

    email_input.fill(registered_user.email)
    password_input.fill(registered_user.password)
    login_button.click()

    logged_in_user = page.get_by_text(
        f"Logged in as {registered_user.name}"
    )

    expect(logged_in_user).to_be_visible()