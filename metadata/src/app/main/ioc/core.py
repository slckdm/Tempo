from dishka import Provider, Scope, provide

from toolkit.common.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from toolkit.common.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from toolkit.common.adapters.redis_cacher import RedisCacher
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.common.services.current_user_service import CurrentUserService

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.services.metadata_service import MetadataService
from app.core.queries.get_track_metadata import GetTrackMetadata
from app.core.queries.get_tracks_metadata import GetTracksMetadata
from app.core.queries.ports.metadata_reader import MetadataReader
from app.outbound.adapters.sqla_metadata_reader import SQLAMetadataReader
from app.outbound.adapters.sqla_metadata_storage import SQLAMetadataStorage


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
    cacher = provide(RedisCacher, provides=Cacher)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(SQLAMetadataStorage, provides=MetadataStorage)
    metadata_service = provide(MetadataService)
    metadata_reader = provide(SQLAMetadataReader, provides=MetadataReader)

    # commands
    get_track_metadata = provide(GetTrackMetadata)
    get_tracks_metadata = provide(GetTracksMetadata)
