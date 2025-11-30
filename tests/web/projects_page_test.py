import pytest

from src.web.Application import Application
from src.web.components.ProjectCard import Badges


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: Application):
    """Test page header functionality"""
    logged_app.projects_page.open()

    logged_app.projects_page.is_loaded()

    logged_app.projects_page.header.check_selected_company("QA Club Lviv")
    logged_app.projects_page.header.plan_name_should_be("Enterprise plan")

    target_project_name = "python manufacture"
    logged_app.projects_page.header.search_project(target_project_name)
    logged_app.projects_page.count_of_project_visible(1)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.Demo)
