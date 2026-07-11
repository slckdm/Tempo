
from dishka import Provider, Scope, provide
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.transaction import Transaction

from app.core.commands.fail_upload import FailUpload
from app.core.commands.finish_upload import FinishUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
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
