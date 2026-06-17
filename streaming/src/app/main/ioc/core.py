from dishka import Provider, Scope, provide

from app.core.commands.stream_audio import StreamAudio
from app.core.ports.audio_storage import AudioStorage
from app.outbound.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.ports.auth_user_finder import AuthorizedUserFinder
from app.outbound.ports.identity_provider import IdentityProvider
from app.outbound.s3_audio_storage import S3AudioStorage


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # Services
    # provide()

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # ports
    audio_storage = provide(S3AudioStorage, provides=AudioStorage)

    # commands
    stream_audio = provide(StreamAudio)
