import pytest
from playwright.sync_api import BrowserContext


@pytest.fixture(autouse=True)
def block_third_party_ads(context: BrowserContext) -> None:
    blocked_domains = (
        "googleads.g.doubleclick.net",
        "pagead2.googlesyndication.com",
        "tpc.googlesyndication.com",
    )

    def handle_route(route) -> None:
        if any(domain in route.request.url for domain in blocked_domains):
            route.abort()
        else:
            route.continue_()

    context.route("**/*", handle_route)