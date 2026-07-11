from typing import Sequence

from fastapi.security import OAuth2, OAuth2PasswordBearer

from dishka import Provider, Scope, collect, provide

from toolkit.common.services.authorization_service import AuthorizationService
from toolkit.config.settings import KeycloakSettings
from toolkit.providers.keycloak_client_provider import KeycloakClientProvider
from toolkit.providers.postgres_provider import PostgresProvider
from toolkit.providers.redis_provider import RedisClientProvider


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=OAuth2)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl=config.token_url, auto_error=False)

    auth_schemas = collect(OAuth2)
    auth_service = provide(AuthorizationService)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        PostgresProvider(),
        KeycloakClientProvider(),
        RedisClientProvider(),
        AuthProvider(),
    )
