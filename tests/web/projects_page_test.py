from playwright.sync_api import Page

from src.web.components.ProjectCard import Badges
from src.web.pages.ProjectsPage import ProjectsPage


def test_projects_page_header(page: Page, login):
    """Test page header functionality"""
    projects_page = ProjectsPage(page)
    projects_page.navigate()

    projects_page.verify_page_loaded()

    projects_page.header.check_selected_company("QA Club Lviv")
    projects_page.header.plan_name_should_be("Enterprise plan")

    target_project_name = "python manufacture"
    projects_page.header.search_project(target_project_name)
    projects_page.count_of_project_visible(1)
    target_project = projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.Demo)
