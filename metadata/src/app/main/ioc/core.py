from dishka import Provider, Scope, provide

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from tempo_toolkit.application.cache import Cache
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.cache import RedisCache
from tempo_toolkit.infrastructure.database import SQLAlchemyFlusher, SQLAlchemyTransaction
from tempo_toolkit.infrastructure.identity import (
    KeycloakAuthorizedUserFinder,
    KeycloakIdentityProvider,
)
from tempo_toolkit.infrastructure.time import SystemUTCTimer

from app.core.commands.healthcheck import Healthcheck
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
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    cacher = provide(RedisCache, provides=Cache)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(SQLAMetadataStorage, provides=MetadataStorage)
    metadata_service = provide(MetadataService)
    metadata_reader = provide(SQLAMetadataReader, provides=MetadataReader)

    # commands
    healthcheck = provide(Healthcheck)
    get_track_metadata = provide(GetTrackMetadata)
    get_tracks_metadata = provide(GetTracksMetadata)
