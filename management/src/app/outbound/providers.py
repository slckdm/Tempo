from typing import Iterable

from dishka import Provider

from .keycloak_client_provider import KeycloakClientProvider
from .postgres_provider import PostgresProvider
from .redis_client_provider import RedisClientProvider
from .s3_provider import S3Provider


def get_outbound_providers() -> Iterable[Provider]:
    return (
        PostgresProvider(),
        S3Provider(),
        RedisClientProvider(),
        KeycloakClientProvider()
    )
