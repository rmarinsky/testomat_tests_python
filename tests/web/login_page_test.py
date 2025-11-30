import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


@pytest.mark.smoke
@pytest.mark.web
def test_login_invalid(app: Application, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, Faker().password(length=10))
    app.login_page.invalid_login_message_visible()


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(app: Application, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login(configs.email, configs.password)

    app.projects_page.is_loaded()