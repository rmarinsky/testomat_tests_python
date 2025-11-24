from src.web.Application import Application
from src.web.components.ProjectCard import Badges


def test_projects_page_header(app: Application, login):
    """Test page header functionality"""
    app.projects_page.navigate()

    app.projects_page.verify_page_loaded()

    app.projects_page.header.check_selected_company("QA Club Lviv")
    app.projects_page.header.plan_name_should_be("Enterprise plan")

    target_project_name = "python manufacture"
    app.projects_page.header.search_project(target_project_name)
    app.projects_page.count_of_project_visible(1)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project.badges_has(Badges.Demo)
