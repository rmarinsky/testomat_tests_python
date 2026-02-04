from src.api.controllers.base_controller import BaseController
from src.api.models import Test


class TestController(BaseController):
    def create(
        self,
        project_id: str,
        suite_id: str,
        title: str,
        description: str | None = None,
    ) -> Test:
        attributes: dict = {"title": title, "suite_id": suite_id}
        if description:
            attributes["description"] = description

        data = self._post(
            f"/api/{project_id}/tests",
            {"data": {"type": "tests", "attributes": attributes}},
        )
        return Test.model_validate(data["data"])

    def get_by_id(self, project_id: str, test_id: str) -> Test:
        data = self._get(f"/api/{project_id}/tests/{test_id}")
        return Test.model_validate(data["data"])

    def update(
        self,
        project_id: str,
        test_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> Test:
        attributes = {}
        if title:
            attributes["title"] = title
        if description:
            attributes["description"] = description

        data = self._put(
            f"/api/{project_id}/tests/{test_id}",
            {"data": {"type": "tests", "attributes": attributes}},
        )
        return Test.model_validate(data["data"])

    def delete(self, project_id: str, test_id: str) -> None:
        self._delete(f"/api/{project_id}/tests/{test_id}")
