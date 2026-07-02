"""Module: S3 Client."""

from typing import Sequence

from fastapi.security import APIKeyCookie, OAuth2, OAuth2PasswordBearer

from dishka import Provider, Scope, collect, provide

from toolkit.clients import KeycloakClient, KeycloakConfig
from toolkit.s3 import S3Client

from app.core.common.auth.service import AuthorizationService
from app.main.config.settings import KeycloakSettings, S3Settings


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def get_client(self, config: S3Settings) -> S3Client:
        return S3Client(
            region_name=config.REGION_NAME,
            url=config.URL,
            access_key_id=config.ACCESS_KEY,
            secret_access_key=config.SECRET_KEY,
        )


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
    return (S3Provider(), AuthProvider(), KeycloakClientProvider())
