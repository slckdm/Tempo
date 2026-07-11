"""Keycloak HTTP client."""

from dataclasses import dataclass
from http import HTTPMethod, HTTPStatus

import aiohttp


class APIClientError(Exception):
    """HTTP API request failed."""

    def __init__(self, status_code: HTTPStatus, data: dict) -> None:
        """Initialize an API error from its status and payload."""
        self.status_code = status_code
        self.data = data
        super().__init__(str(status_code))


class APIClient:
    """Minimal asynchronous JSON API client."""

    def __init__(self, base_url: str) -> None:
        """Initialize a client with its base URL."""
        self.base_url = base_url

    async def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: dict | None = None,
        payload: dict | None = None,
        data: dict | None = None,
        query: dict | None = None,
    ) -> dict:
        """Perform an HTTP request and return its JSON payload."""
        async with aiohttp.ClientSession(self.base_url, headers=headers or {}) as session:
            async with session.request(
                method, endpoint, params=query, json=payload, data=data
            ) as response:
                response_data = await response.json()
                if response.status >= 400:
                    raise APIClientError(response.status, response_data)
                return response_data


@dataclass
class KeycloakConfig:
    """Keycloak client configuration."""

    url: str
    realm: str
    client_id: str
    client_secret: str
    token_url: str


class KeycloakClient(APIClient):
    """Keycloak administrative API client."""

    def __init__(self, configuration: KeycloakConfig) -> None:
        """Initialize a Keycloak client."""
        super().__init__(configuration.url)
        self._configuration = configuration

    async def get_jwk(self) -> str:
        """Return the realm public key."""
        payload = await self.request(
            HTTPMethod.GET, f"{self.base_url}/realms/{self._configuration.realm}"
        )
        return payload["public_key"]

    async def authorize(self) -> str:
        """Get a service-account access token."""
        payload = await self.request(
            HTTPMethod.POST,
            self._configuration.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self._configuration.client_id,
                "client_secret": self._configuration.client_secret,
                "grant_type": "client_credentials",
            },
        )
        return payload["access_token"]

    async def get_user_by_id(self, user_id: str) -> dict:
        """Return Keycloak user data."""
        token = await self.authorize()
        endpoint = f"{self.base_url}/admin/realms/{self._configuration.realm}/users/{user_id}"
        return await self.request(
            HTTPMethod.GET, endpoint, headers={"Authorization": f"Bearer {token}"}
        )
