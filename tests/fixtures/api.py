import pytest

from src.api.client import ApiClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    client = ApiClient(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
    )
    client._authenticate()
    yield client
    client.close()
