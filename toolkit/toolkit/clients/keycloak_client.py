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
        self.configuration = configuration

    async def get_jwk(self) -> str:
        """Retrieve JSON Web Key.

        Returns:
            str: JSON Web Key value.
        """
        url = self.configuration.url + "/realms/" + self.configuration.realm
        payload = await self.request(HTTPMethod.GET, url)
        return payload["public_key"]
