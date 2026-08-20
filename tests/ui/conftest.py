from collections.abc import Iterator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import BrowserContext
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

    if report.when != "call":
        return

    item.test_failed = report.failed

    if not report.failed:
        return

    page = item.funcargs.get("page")
    context = item.funcargs.get("context")

    if page is None or context is None:
        return

    evidence_dir = Path("test-results")
    evidence_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    screenshot_path = evidence_dir / f"{item.name}-screenshot.png"
    trace_path = evidence_dir / f"{item.name}-trace.zip"

    page.screenshot(
        path=screenshot_path,
    )

    allure.attach.file(
        source=screenshot_path,
        name="Failure screenshot",
        attachment_type=allure.attachment_type.PNG,
    )

    context.tracing.stop(
        path=trace_path,
    )

    allure.attach.file(
        source=trace_path,
        name="Playwright trace",
        attachment_type="application/zip",
    )

    item.trace_stopped = True


@pytest.fixture(autouse=True)
def capture_trace_on_failure(
    request: FixtureRequest,
    context: BrowserContext,
) -> Iterator[None]:
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield

    trace_stopped = getattr(
        request.node,
        "trace_stopped",
        False,
    )

    if not trace_stopped:
        context.tracing.stop()
