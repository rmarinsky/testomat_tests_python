from playwright.sync_api import Page, expect


class RunsPage:

    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> RunsPage:
        expect(self.page.locator("df")).to_be_visibile()
        return self
