from src.api.client import ApiClient
from src.api.models import Project, ProjectsResponse


class TestAuthentication:
    def test_login_with_valid_token(self, api_client: ApiClient):
        """Test that authentication with valid API token returns JWT."""
        jwt_token = api_client._authenticate()

        assert jwt_token is not None
        assert isinstance(jwt_token, str)
        assert len(jwt_token) > 0

    def test_jwt_token_is_cached(self, api_client: ApiClient):
        """Test that JWT token is cached after first authentication."""
        first_token = api_client._authenticate()
        second_token = api_client._authenticate()

        assert first_token == second_token


class TestGetProjects:
    def test_get_projects_returns_response(self, api_client: ApiClient):
        """Test that get_projects returns ProjectsResponse."""
        response = api_client.get_projects()

        assert response is not None
        assert isinstance(response, ProjectsResponse)

    def test_get_projects_returns_list_of_projects(self, api_client: ApiClient):
        """Test that projects data is a list of Project objects."""
        response = api_client.get_projects()

        assert isinstance(response.data, list)
        if len(response) > 0:
            assert isinstance(response[0], Project)

    def test_project_has_required_attributes(self, api_client: ApiClient):
        """Test that each project has required attributes."""
        response = api_client.get_projects()

        if len(response) > 0:
            project = response[0]
            assert project.id is not None
            assert project.type == "project"
            assert project.title is not None
            assert project.status is not None

    def test_projects_response_is_iterable(self, api_client: ApiClient):
        """Test that ProjectsResponse can be iterated."""
        projects = api_client.get_projects()

        for project in projects:
            print(f"{project.id}")
            print(f"{project.title} - {project.status}")
            print(f"Tests: {project.tests_count}")
