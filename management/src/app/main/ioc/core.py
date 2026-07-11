from dishka import Provider, Scope, provide
from toolkit.common.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from toolkit.common.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from toolkit.common.adapters.redis_cacher import RedisCacher
from toolkit.common.adapters.s3_object_storage import S3ObjectStorage
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.outbox.adapters.sqla_outbox_storage import SQLAOutboxStorage
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.service import OutboxService

from app.core.commands.complete_upload import CompleteUpload
from app.core.commands.create_upload import CreateUpload
from app.core.commands.delete_upload import DeleteUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)
    cacher = provide(RedisCacher, provides=Cacher)

    # Services
    current_user_service = provide(CurrentUserService)
    upload_service = provide(UploadService)
    outbox_service = provide(OutboxService)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)
    outbox_storage = provide(SQLAOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    create_upload = provide(CreateUpload)
    complete_upload = provide(CompleteUpload)
    delete_upload = provide(DeleteUpload)
