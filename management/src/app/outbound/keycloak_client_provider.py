from dishka import Provider, Scope, provide

from toolkit.clients import KeycloakClient, KeycloakConfig

from app.main.config.settings import KeycloakSettings


class KeycloakClientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def new_client(self, config: KeycloakSettings) -> KeycloakClient:
        return KeycloakClient(
            KeycloakConfig(
                url=config.URL,
                realm=config.REALM,
                client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                token_url=config.token_url,
            )
        )
