import os

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    """Shared browser instance for the entire test session."""
    headless = os.getenv("CI", "false").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=0, timeout=30000)
        yield browser
        browser.close()
