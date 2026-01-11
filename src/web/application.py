from playwright.sync_api import Page

from .pages.home_page import HomePage
from .pages.login_page import LoginPage
from .pages.new_projects_page import NewProjectsPage
from .pages.project_page import ProjectPage
from .pages.projects_page import ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_projects_page = NewProjectsPage(page)
        self.project_page = ProjectPage(page)
