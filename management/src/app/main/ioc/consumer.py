
from dishka import Provider, Scope, provide

from app.core.commands.fail_upload import FailUpload
from app.core.commands.finish_upload import FinishUpload
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # ports
    transaction = provide(SQLATransaction, provides=Transaction)
    flusher = provide(SQLAFlusher, provides=Flusher)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)

    # services
    upload_service = provide(UploadService)

    # commands
    finish_upload = provide(FinishUpload)
    fail_upload = provide(FailUpload)
