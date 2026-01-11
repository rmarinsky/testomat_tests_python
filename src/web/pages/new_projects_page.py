from typing import TYPE_CHECKING, Self

from playwright.sync_api import Page, expect

if TYPE_CHECKING:
    from .project_page import ProjectPage


class NewProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self._form_container = page.locator("#content-desktop [action='/projects']")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def is_loaded(self) -> Self:
        expect(self._form_container).to_be_visible()
        project_label_classical = self._form_container.locator("#classical")
        expect(project_label_classical).to_be_visible()
        expect(project_label_classical).to_contain_text("Classical")

        project_label_bdd = self._form_container.locator("#bdd")
        expect(project_label_bdd).to_be_visible()
        expect(project_label_bdd).to_contain_text("BDD")

        expect(self._form_container.locator("#project_title")).to_be_visible()
        expect(self._form_container.locator("#demo-btn")).to_be_visible()
        expect(self._form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    def fill_project_title(self, target_project_name: str) -> Self:
        self._form_container.locator("#project_title").fill(target_project_name)
        return self

    def click_create(self) -> "ProjectPage":
        from .project_page import ProjectPage

        self._form_container.locator("#project-create-btn input").click()
        expect(self._form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return ProjectPage(self.page)
