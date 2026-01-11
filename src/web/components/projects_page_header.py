from typing import Self

from playwright.sync_api import Page, expect


class ProjectsPageHeader:
    """Component for projects page header section"""

    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.locator('h2', has_text='Projects')
        self.company_selector = page.locator('#company_id')
        self.plan_badge = page.locator('.tooltip-project-plan')

        self.search_input = page.locator('#search')

        self.create_button = page.locator('a.common-btn-primary', has_text='Create')
        self.manage_button = page.locator('a.common-btn-secondary', has_text='Manage')

        self.grid_view_button = page.locator('#grid-view')
        self.table_view_button = page.locator('#table-view')

    def select_company(self, company_name: str) -> Self:
        self.company_selector.select_option(label=company_name)
        return self

    def search_project(self, query: str) -> Self:
        self.search_input.fill(query)
        return self

    def click_create(self) -> Self:
        self.create_button.click()
        return self

    def click_manage(self) -> Self:
        self.manage_button.click()
        return self

    def switch_to_grid_view(self) -> Self:
        self.grid_view_button.click()
        return self

    def switch_to_table_view(self) -> Self:
        self.table_view_button.click()
        return self

    def check_selected_company(self, expected_value: str) -> Self:
        expect(self.company_selector.locator('option[selected]')).to_have_text(expected_value)
        return self

    def plan_name_should_be(self, expected_value: str) -> Self:
        expect(self.plan_badge.locator('span').last).to_have_text(expected_value)
        return self
