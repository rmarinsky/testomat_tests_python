from typing import Self

import allure
from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step
    def open(self) -> Self:
        self.page.goto("https://testomat.io")
        return self

    @allure.step
    def is_loaded(self) -> Self:
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_have_text("Log in")
        expect(self.page.locator(".side-menu .start-item")).to_have_text("Start for free")
        return self

    @allure.step
    def click_login(self) -> Self:
        self.page.get_by_text("Log in", exact=True).click()
        return self
