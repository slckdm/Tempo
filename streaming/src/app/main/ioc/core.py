from dishka import Provider, Scope, provide

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.services.current_user_service import CurrentUserService
from app.core.queries.ports.object_storage import ObjectStorage
from app.core.queries.stream import Stream
from app.outbound.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.adapters.s3_object_storage import S3ObjectStorage


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # Services
    current_user_service = provide(CurrentUserService)

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # ports
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    stream = provide(Stream)
