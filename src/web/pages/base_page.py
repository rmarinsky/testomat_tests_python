from abc import ABC, abstractmethod
from typing import Self

from playwright.sync_api import Page


class BasePage(ABC):
    """Base class for all page objects providing common functionality."""

    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def is_loaded(self) -> Self:
        """Verify that the page is loaded. Must be implemented by subclasses."""
        ...

    def wait_for_load(self, timeout: int = 30000) -> Self:
        """Wait for the page to finish loading."""
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        return self

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def take_screenshot(self, path: str) -> Self:
        """Take a screenshot of the current page."""
        self.page.screenshot(path=path)
        return self

    def scroll_to_top(self) -> Self:
        """Scroll to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")
        return self

    def scroll_to_bottom(self) -> Self:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        return self
