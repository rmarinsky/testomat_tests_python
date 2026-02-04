import pytest
import requests

from src.api.controllers import ProjectController, SuiteController, TestController
from src.api.models import Project
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def auth_token(configs: Config) -> str:
    """Single authentication token shared across all controllers."""
    response = requests.post(
        f"{configs.app_base_url}/api/login",
        json={"api_token": configs.testomat_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_controller(configs: Config, auth_token: str) -> ProjectController:
    controller = ProjectController(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def suite_controller(configs: Config, auth_token: str) -> SuiteController:
    controller = SuiteController(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def test_controller(configs: Config, auth_token: str) -> TestController:
    controller = TestController(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="function")
def project(project_controller: ProjectController) -> Project:
    """Get the first available project as a precondition."""
    projects = project_controller.get_all()
    return projects[0]
