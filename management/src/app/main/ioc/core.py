from dishka import Provider, Scope, provide

from app.core.commands.complete_upload import CompleteUpload
from app.core.commands.create_upload import CreateUpload
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.cacher import Cacher
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.outbox_service import OutboxService
from app.core.common.services.upload_service import UploadService
from app.outbound.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.adapters.redis_cacher import RedisCacher
from app.outbound.adapters.s3_object_storage import S3ObjectStorage
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_outbox_storage import SQLAOutboxStorage
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage
from app.outbound.adapters.system_utc_timer import SystemUTCTimer


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
