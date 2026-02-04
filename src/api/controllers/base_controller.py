import logging

import requests

logger = logging.getLogger(__name__)


class BaseController:
    def __init__(self, base_url: str, api_token: str, jwt_token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = requests.Session()
        self._jwt_token: str | None = jwt_token

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _authenticate(self) -> str:
        if self._jwt_token:
            return self._jwt_token

        url = self._url("/api/login")
        logger.info("POST %s | Body: {api_token: ***}", url)
        response = self._client.post(
            url,
            json={"api_token": self.api_token},
            timeout=30,
        )
        logger.info("Response [%s]: %s", response.status_code, response.text)
        self._jwt_token = response.json()["jwt"]
        return self._jwt_token

    def _headers(self) -> dict[str, str]:
        return {"Authorization": self._authenticate(), "Content-Type": "application/json"}

    def _get(self, endpoint: str) -> dict:
        url = self._url(endpoint)

        logger.info("GET %s", url)

        response = self._client.get(url, headers=self._headers(), timeout=30)

        logger.info("Response [%s]: %s", response.status_code, response.json())

        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict) -> dict:
        url = self._url(endpoint)

        logger.info("POST %s | Body: %s", url, data)
        response = self._client.post(url, headers=self._headers(), json=data, timeout=30)

        logger.info("Response [%s]: %s", response.status_code, response.json())
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, data: dict) -> dict:
        url = self._url(endpoint)
        logger.info("PUT %s | Body: %s", url, data)
        response = self._client.put(url, headers=self._headers(), json=data, timeout=30)
        logger.info("Response [%s]: %s", response.status_code, response.json())
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint: str) -> None:
        url = self._url(endpoint)
        logger.info("DELETE %s", url)
        response = self._client.delete(url, headers=self._headers(), timeout=30)
        logger.info("Response [%s]: %s", response.status_code, response.text)
        response.raise_for_status()

    def close(self) -> None:
        self._client.close()
