from typing import Sequence

from fastapi.security import APIKeyCookie, OAuth2, OAuth2PasswordBearer

from dishka import Provider, Scope, collect, provide

from toolkit.common.services.authorization_service import AuthorizationService
from toolkit.config.settings import KeycloakSettings
from toolkit.providers.keycloak_client_provider import KeycloakClientProvider
from toolkit.providers.redis_provider import RedisClientProvider
from toolkit.providers.s3_provider import S3Provider


class AuthProvider(Provider):
    scope = Scope.REQUEST
    ACCESS_TOKEN_COOKIE = "access_token"

    @provide(provides=OAuth2)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl=config.token_url, auto_error=False)

    @provide(provides=OAuth2)
    def provide_cookie_schema(self) -> APIKeyCookie:
        return APIKeyCookie(name=self.ACCESS_TOKEN_COOKIE, auto_error=False)

    auth_schemas = collect(OAuth2)
    auth_service = provide(AuthorizationService)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        AuthProvider(),
        RedisClientProvider(),
        S3Provider(),
        KeycloakClientProvider(),
    )
