from src.api.controllers.base_controller import BaseController
from src.api.models import Project, ProjectsResponse


class ProjectController(BaseController):
    def get_all(self) -> ProjectsResponse:
        data = self._get("/api/projects")
        return ProjectsResponse.model_validate(data)

    def get_by_id(self, project_id: str) -> Project:
        data = self._get(f"/api/project/{project_id}")
        return Project.model_validate(data["data"])
