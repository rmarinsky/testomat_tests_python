from typing import Self

from playwright.sync_api import Page, expect

from ..components import SideBar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible(timeout=10000)
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.locator("[placeholder='First Suite']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Suite")).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name)
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self

    def create_test_via_popup(self):
        self.page.locator(".sticky-header").get_by_role("button", name="Test  ", exact=True).click()
        return self

    def create_first_suite(self, target_suite_name: str):
        self.page.locator("[placeholder='First Suite']").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()
        expect(suite_button).to_be_hidden()
        return self
