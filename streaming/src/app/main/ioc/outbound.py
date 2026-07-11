from typing import Sequence

from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from fastapi.security.base import SecurityBase

from dishka import Provider, Scope, collect, provide

from tempo_toolkit.application.auth import TokenProvider
from tempo_toolkit.infrastructure.cache import RedisClientProvider
from tempo_toolkit.infrastructure.identity import KeycloakClientProvider, KeycloakSettings
from tempo_toolkit.infrastructure.object_storage import S3Provider
from tempo_toolkit.infrastructure.web import FastAPITokenProvider


class AuthProvider(Provider):
    scope = Scope.REQUEST
    ACCESS_TOKEN_COOKIE = "access_token"

    @provide(provides=SecurityBase)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl=config.token_url, auto_error=False)

    @provide(provides=SecurityBase)
    def provide_cookie_schema(self) -> APIKeyCookie:
        return APIKeyCookie(name=self.ACCESS_TOKEN_COOKIE, auto_error=False)

    auth_schemas = collect(SecurityBase)
    token_provider = provide(FastAPITokenProvider, provides=TokenProvider)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        AuthProvider(),
        RedisClientProvider(),
        S3Provider(),
        KeycloakClientProvider(),
    )
