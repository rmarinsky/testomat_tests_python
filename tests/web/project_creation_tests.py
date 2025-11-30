import pytest
from faker import Faker

from src.web.Application import Application


@pytest.mark.regression
@pytest.mark.web
def test_new_project_creation_and_test_popup(login, app: Application):
    target_project_name = Faker().company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    project_page = app.project_page
    (project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (project_page.side_bar
     .is_loaded()
     .click_logo()
     .expect_tab_active("Tests"))

    target_suite_name = Faker().company()
    project_page.create_first_suite(target_suite_name)
    project_page.create_test()
