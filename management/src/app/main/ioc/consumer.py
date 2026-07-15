from dishka import Provider, Scope, provide

from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.database import (
    SQLAlchemyFlusher,
    SQLAlchemyOutboxStorage,
    SQLAlchemyTransaction,
)
from tempo_toolkit.infrastructure.time import SystemUTCTimer

from app.core.commands.fail_upload import FailUpload
from app.core.commands.finish_upload import FinishUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # ports
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)
    outbox_storage = provide(SQLAlchemyOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # services
    upload_service = provide(UploadService)
    outbox_service = provide(OutboxService)

    # commands
    finish_upload = provide(FinishUpload)
    fail_upload = provide(FailUpload)
