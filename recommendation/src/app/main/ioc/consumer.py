from dishka import Provider, Scope, provide

from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.database import (
    SQLAlchemyFlusher,
    SQLAlchemyOutboxStorage,
    SQLAlchemyTransaction,
)
from tempo_toolkit.infrastructure.object_storage import S3ObjectStorage
from tempo_toolkit.infrastructure.time import SystemUTCTimer

from app.core.commands.delete_track_features import DeleteSongFeatures
from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.commands.save_track_features import SaveSongFeatures
from app.outbound.adapters.qdrant_feature_storage import QdrantFeatureStorage


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # ports
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(QdrantFeatureStorage, provides=FeatureStorage)
    outbox_service = provide(OutboxService)
    outbox_storage = provide(SQLAlchemyOutboxStorage, provides=OutboxStorage)
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    save_features = provide(SaveSongFeatures)
    delete_features = provide(DeleteSongFeatures)
