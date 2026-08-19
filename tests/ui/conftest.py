from collections.abc import Iterator
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page
from pytest import FixtureRequest


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.test_failed = report.failed


@pytest.fixture(autouse=True)
def capture_trace_on_failure(
    request: FixtureRequest,
    context: BrowserContext,
    page: Page,
) -> Iterator[None]:
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield

    failed = getattr(
        request.node,
        "test_failed",
        False,
    )

    if failed:
        evidence_dir = Path("test-results")
        trace_path = evidence_dir / f"{request.node.name}-trace.zip"
        screenshot_path = evidence_dir / f"{request.node.name}-screenshot.png"

        evidence_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        page.screenshot(
            path=screenshot_path,
        )

        context.tracing.stop(
            path=trace_path,
        )
    else:
        context.tracing.stop()