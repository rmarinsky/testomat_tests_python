import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.web.application import Application

load_dotenv()


def clear_browser_state(page: Page) -> None:
    """Clear cookies and local storage for the current page context."""
    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


# Shared browser instance for session
@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0, timeout=30000)
        yield browser
        browser.close()


# 1. Clean app - fresh page per test (function scope)
@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Application:
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


# 2. Logged app - reuses authenticated session (session scope)
@pytest.fixture(scope="session")
def logged_context(browser_instance: Browser, configs: Config) -> BrowserContext:
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext) -> Application:
    page = logged_context.new_page()
    page.goto("/projects")
    yield Application(page)
    page.close()


# 3. Shared page for parametrized tests (module scope) - reuses same page across test params
@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs) -> Page:
    context = build_browser_instance(browser_instance, configs)

    page = context.new_page()
    yield page
    page.close()
    context.close()


def build_browser_instance(browser_instance: Browser, configs: Config) -> BrowserContext:
    return browser_instance.new_context(
        base_url=configs.app_base_url,
        viewport={"width": 1920, "height": 1080},
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="test-result/videos/",
        permissions=["geolocation"],
    )


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Application:
    yield Application(shared_browser)
    clear_browser_state(shared_browser)
