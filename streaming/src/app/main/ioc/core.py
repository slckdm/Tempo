from dishka import Provider, Scope, provide

from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.stream_audio import StreamAudio
from app.core.commands.stream_cover import StreamCover
from app.outbound.adapters.s3_object_storage import S3ObjectStorage
from app.outbound.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.ports.auth_user_finder import AuthorizedUserFinder
from app.outbound.ports.identity_provider import IdentityProvider


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # Services

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # ports
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    stream_audio = provide(StreamAudio)
    stream_cover = provide(StreamCover)
