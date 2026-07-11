"""Keycloak Dishka provider."""

from dishka import Provider, Scope, provide

from .client import KeycloakClient, KeycloakConfig
from .settings import KeycloakSettings


class KeycloakClientProvider(Provider):
    """Provide request-scoped Keycloak clients."""

    @provide(scope=Scope.REQUEST)
    def new_client(self, config: KeycloakSettings) -> KeycloakClient:
        """Create a Keycloak client."""
        return KeycloakClient(
            KeycloakConfig(
                url=config.URL,
                realm=config.REALM,
                client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                token_url=config.token_url,
            )
        )
