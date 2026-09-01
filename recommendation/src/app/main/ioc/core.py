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
from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.queries.get_similar_tracks import GetSimilarTracks
from app.core.queries.ports.feature_reader import FeatureReader
from app.outbound.adapters.qdrant_feature_reader import QdrantFeatureReader
from app.outbound.adapters.qdrant_feature_storage import QdrantFeatureStorage


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)
    feature_storage = provide(QdrantFeatureStorage, provides=FeatureStorage)
    feature_reader = provide(QdrantFeatureReader, provides=FeatureReader)

    # Services
    current_user_service = provide(CurrentUserService)

    # ports
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    cacher = provide(RedisCache, provides=Cache)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    healthcheck = provide(Healthcheck)
    get_similar_tracks = provide(GetSimilarTracks)
