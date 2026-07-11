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

from app.core.commands.delete_track_metadata import DeleteTrackMetadata
from app.core.commands.fail_metadata import FailMetadata
from app.core.commands.ports.metadata_parser import MetadataParser
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.process_track_metadata import ProcessTrackMetadata
from app.core.common.services.metadata_service import MetadataService
from app.outbound.adapters.sqla_metadata_storage import SQLAMetadataStorage
from app.outbound.adapters.tinytag_metadata_parser import TinyTagMetadataParser


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # ports
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(SQLAMetadataStorage, provides=MetadataStorage)
    metadata_service = provide(MetadataService)
    outbox_service = provide(OutboxService)
    metadata_reader = provide(TinyTagMetadataParser, provides=MetadataParser)
    outbox_storage = provide(SQLAlchemyOutboxStorage, provides=OutboxStorage)
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    process_metadata = provide(ProcessTrackMetadata)
    fail_metadata = provide(FailMetadata)
    delete_metadata = provide(DeleteTrackMetadata)
