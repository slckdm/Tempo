from dishka import Provider, Scope, provide

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.commands.ports.flusher import Flusher
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.metadata_service import MetadataService
from app.core.queries.get_track_metadata import GetTrackMetadata
from app.core.queries.get_tracks_metadata import GetTracksMetadata
from app.core.queries.ports.metadata_reader import MetadataReader
from app.outbound.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_metadata_reader import SQLAMetadataReader
from app.outbound.adapters.sqla_metadata_storage import SQLAMetadataStorage
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.system_utc_timer import SystemUTCTimer


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # Services
    current_user_service = provide(CurrentUserService)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(SQLAMetadataStorage, provides=MetadataStorage)
    metadata_service = provide(MetadataService)
    metadata_reader = provide(SQLAMetadataReader, provides=MetadataReader)

    # commands
    get_track_metadata = provide(GetTrackMetadata)
    get_tracks_metadata = provide(GetTracksMetadata)
