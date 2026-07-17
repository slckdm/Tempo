from dishka import Provider, Scope, provide

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from tempo_toolkit.application.cache import Cache
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.infrastructure.cache import RedisCache
from tempo_toolkit.infrastructure.identity import (
    KeycloakAuthorizedUserFinder,
    KeycloakIdentityProvider,
)
from tempo_toolkit.infrastructure.object_storage import S3ObjectStorage

from app.core.commands.healthcheck import Healthcheck
from app.core.queries.stream import Stream


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # Services
    current_user_service = provide(CurrentUserService)

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)
    cacher = provide(RedisCache, provides=Cache)

    # ports
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    healthcheck = provide(Healthcheck)
    stream = provide(Stream)
