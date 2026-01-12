from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.fixtures.cookie_helper import (
    CookieHelper,
    clear_browser_state,
)

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")


def build_browser_context(browser: Browser, base_url: str) -> BrowserContext:
    """Build a new browser context with standard configuration."""
    return browser.new_context(
        base_url=base_url,
        viewport={"width": 1920, "height": 1080},
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="test-result/videos/",
        permissions=["geolocation"],
    )


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs) -> Application:
    """Clean app - fresh page per test (function scope)."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs) -> BrowserContext:
    """Logged context - reuses authenticated session (session scope)."""
    context = build_browser_context(browser_instance, configs.app_base_url)

    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    # Save storage state after successful login
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)

    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext) -> Application:
    """Logged app - new page from authenticated context for each test."""
    page = logged_context.new_page()
    page.goto("/projects")
    yield Application(page)
    page.close()


@pytest.fixture(scope="function")
def cookies(logged_context: BrowserContext) -> CookieHelper:
    """Provides cookie manipulation helper for the logged-in context."""
    return CookieHelper(logged_context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs) -> Page:
    """Shared page for parametrized tests (module scope) - reuses same page across test params."""
    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Application:
    """Shared page with state clearing between tests."""
    yield Application(shared_browser)
    clear_browser_state(shared_browser)
