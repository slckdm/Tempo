from dishka import Provider, Scope, provide

from toolkit.common.adapters.s3_object_storage import S3ObjectStorage
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.outbox.adapters.sqla_outbox_storage import SQLAOutboxStorage
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.service import OutboxService

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
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    metadata_storage = provide(SQLAMetadataStorage, provides=MetadataStorage)
    metadata_service = provide(MetadataService)
    outbox_service = provide(OutboxService)
    metadata_reader = provide(TinyTagMetadataParser, provides=MetadataParser)
    outbox_storage = provide(SQLAOutboxStorage, provides=OutboxStorage)
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)

    # commands
    process_metadata = provide(ProcessTrackMetadata)
    fail_metadata = provide(FailMetadata)
    delete_metadata = provide(DeleteTrackMetadata)
