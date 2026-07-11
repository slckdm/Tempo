"""Module: Keycloak API Client."""

from http import HTTPMethod

from toolkit.clients import APIClient

from .keycloak_configuration import KeycloakConfig


class KeycloakClient(APIClient):
    """Keycloak service API client."""

    def __init__(self, configuration: KeycloakConfig) -> None:
        """Initialize client.

        Args:
            configuration (KeycloakConfig): Configuration object.
        """
        super().__init__(configuration.url)
        self._configuration = configuration
        self._realm = self._configuration.realm

    async def get_jwk(self) -> str:
        """Retrieve JSON Web Key.

        Returns:
            str: JSON Web Key value.
        """
        url = f"{self.base_url}/realms/{self._configuration.realm}"
        payload = await self.request(HTTPMethod.GET, url)
        return payload["public_key"]

    async def authorize(self) -> str:
        payload = await self.request(
            HTTPMethod.POST,
            self._configuration.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self._configuration.client_id,
                "client_secret": self._configuration.client_secret,
                "grant_type": "client_credentials"
            }
        )
        return payload["access_token"]

    async def get_user_by_id(self, id: str) -> dict:
        """Get user data by user identifier."""
        token = await self.authorize()
        url = f"{self.base_url}/admin/realms/{self._configuration.realm}/users/{id}"
        payload = await self.request(
            HTTPMethod.GET, url, headers={"Authorization": f"Bearer {token}"}
        )
        return payload
