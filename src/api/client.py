import requests

from src.api.models.project import ProjectsResponse


class ApiClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = requests.Session()
        self._client.timeout = 30
        self._jwt_token: str | None = None

    def _url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return f"{self.base_url}{endpoint}"

    def _authenticate(self) -> str:
        """Authenticate using API token and return JWT."""
        if self._jwt_token:
            return self._jwt_token

        response = self._client.post(
            self._url("/api/login"),
            json={"api_token": self.api_token},
            timeout=30,
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
            self._url("/api/projects"),
            headers=self._get_auth_headers(),
            timeout=30,
        )
        response.raise_for_status()
        return ProjectsResponse.model_validate(response.json())

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
