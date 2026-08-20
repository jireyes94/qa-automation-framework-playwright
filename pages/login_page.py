from playwright.sync_api import Locator, Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self._page = page

        self.email_input: Locator = page.locator("input[data-qa='login-email']")
        self.password_input: Locator = page.locator("input[data-qa='login-password']")
        self.login_button: Locator = page.get_by_role(
            "button",
            name="Login",
        )
        self.error_message: Locator = page.get_by_text(
            "Your email or password is incorrect!"
        )

    def open(self) -> None:
        self._page.goto("/login")

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
