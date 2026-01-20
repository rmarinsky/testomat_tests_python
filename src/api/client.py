import httpx

from src.api.models.project import ProjectsResponse


class ApiClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_token = api_token
        self._client = httpx.Client(base_url=base_url, timeout=30.0)
        self._jwt_token: str | None = None

    def _authenticate(self) -> str:
        """Authenticate using API token and return JWT."""
        if self._jwt_token:
            return self._jwt_token

        response = self._client.post(
            "/api/login",
            json={"api_token": self.api_token},
        )
        response.raise_for_status()
        self._jwt_token = response.json()["jwt"]
        return self._jwt_token

    def _get_auth_headers(self) -> dict[str, str]:
        """Get authorization headers with JWT token."""
        jwt = self._authenticate()
        return {"Authorization": jwt}

    def get_projects(self) -> ProjectsResponse:
        """Get all projects for the authenticated user."""
        response = self._client.get(
            "/api/projects",
            headers=self._get_auth_headers(),
        )
        response.raise_for_status()
        return ProjectsResponse.from_dict(response.json())

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
