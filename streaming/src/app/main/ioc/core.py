from dishka import Provider, Scope, provide

from toolkit.common.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from toolkit.common.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from toolkit.common.adapters.redis_cacher import RedisCacher
from toolkit.common.adapters.s3_object_storage import S3ObjectStorage
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.services.current_user_service import CurrentUserService

from app.core.queries.stream import Stream


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # Services
    current_user_service = provide(CurrentUserService)

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)
    cacher = provide(RedisCacher, provides=Cacher)

    # ports
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    stream = provide(Stream)
