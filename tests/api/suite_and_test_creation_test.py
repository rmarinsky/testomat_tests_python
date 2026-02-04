import pytest
from faker import Faker

from src.api.controllers import SuiteController, TestController
from src.api.models import Project

fake = Faker()


@pytest.mark.smoke
@pytest.mark.api
def test_create_suite(
    project: Project,
    suite_controller: SuiteController,
    test_controller: TestController,
):
    # Create suite
    suite_name = fake.sentence()
    suite_response = suite_controller.create(project_id=project.id, title=suite_name, description=fake.paragraph())

    actual_test_suite = suite_controller.get_by_id(project.id, suite_response.id)

    assert suite_response.id == actual_test_suite.id
    assert suite_response.attributes.title == actual_test_suite.attributes.title
    assert actual_test_suite.attributes.title == suite_name


@pytest.mark.smoke
@pytest.mark.api
def test_create_suite_and_case(
    project: Project,
    suite_controller: SuiteController,
    test_controller: TestController,
):
    # Create suite
    suite_name = fake.sentence()
    suite = suite_controller.create(project_id=project.id, title=suite_name)

    # Precondition: Create test UI
    test_ui_title = fake.sentence()
    test_ui = test_controller.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_ui_title,
    )

    # Create test case
    test_case_title = fake.sentence()
    test_case_description = fake.paragraph()
    test_case = test_controller.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_case_title,
        description=test_case_description,
    )

    # Check response
    assert test_case.id is not None
    assert test_case.title == test_case_title
    assert test_case.type == "test"

    # Cleanup
    test_controller.delete(project.id, test_case.id)
    test_controller.delete(project.id, test_ui.id)
    suite_controller.delete(project.id, suite.id)
