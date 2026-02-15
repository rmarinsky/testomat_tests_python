from typing import Self

import allure
from playwright.sync_api import Page, expect

from ..components.project_card import ProjectCard
from ..components.projects_page_header import ProjectsPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsPageHeader(page)

        self.success_message = page.locator(".common-flash-success-right p")
        self.info_message = page.locator(".common-flash-info-right p")

        self.projects_grid = page.locator("#grid,[src*='no-project.svg']")
        self._project_cards = page.locator('#grid ul li a[href*="/projects/"]')

        self.total_count = page.locator(".common-counter")

    @allure.step
    def open(self, url: str = "/projects") -> Self:
        self.page.goto(url)
        return self

    @allure.step
    def get_success_message(self) -> str:
        return self.success_message.text_content().strip()

    @allure.step
    def get_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self._project_cards.all()]

    @allure.step
    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self._project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        return ProjectCard(card)

    @allure.step
    def count_of_projects_visible(self, expected_count: int) -> Self:
        expect(self._project_cards.filter(visible=True)).to_have_count(expected_count)
        return self

    @allure.step
    def get_total_projects(self) -> int:
        return int(self.total_count.text_content())

    @allure.step
    def search_and_get_results(self, query: str) -> list[ProjectCard]:
        self.header.search_project(query)
        self.page.wait_for_timeout(300)
        return self.get_projects()

    @allure.step
    def is_loaded(self) -> Self:
        expect(self.header.page_title).to_be_visible()
        expect(self.projects_grid.first).to_be_visible()
        return self

    @allure.step
    def verify_success_message(self, expected_text: str) -> Self:
        expect(self.success_message).to_have_text(expected_text)
        return self

    @allure.step
    def get_demo_projects(self) -> list[ProjectCard]:
        return [project for project in self.get_projects() if project.is_demo_project()]
