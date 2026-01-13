import json
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.fixtures.cookie_helper import (
    CookieHelper,
    clear_browser_state,
)

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STORAGE_PATH = Path("test-result/.auth/free_project_state.json")


def create_free_project_state() -> None:
    """Create free project state by copying storage state with empty company_id."""
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FREE_PROJECT_STORAGE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_context(
    browser: Browser,
    base_url: str,
    storage_state: Path | None = None,
) -> BrowserContext:
    kwargs = {
        "base_url": base_url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    return browser.new_context(**kwargs)


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
    if STORAGE_STATE_PATH.exists():
        context = build_browser_context(browser_instance, configs.app_base_url, storage_state=STORAGE_STATE_PATH)
        yield context
        context.close()
        return

    context = build_browser_context(browser_instance, configs.app_base_url)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)

    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_STATE_PATH)
    create_free_project_state()

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


@pytest.fixture(scope="session")
def free_project_context(logged_context: BrowserContext, browser_instance: Browser, configs) -> BrowserContext:
    context = build_browser_context(browser_instance, configs.app_base_url, storage_state=FREE_PROJECT_STORAGE_PATH)
    yield context
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_context: BrowserContext) -> Application:
    page = free_project_context.new_page()
    page.goto("/projects")
    yield Application(page)
    page.close()
