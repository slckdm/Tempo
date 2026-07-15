from dishka import Provider, Scope, provide

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from tempo_toolkit.application.cache import Cache
from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.cache import RedisCache
from tempo_toolkit.infrastructure.database import (
    SQLAlchemyFlusher,
    SQLAlchemyOutboxStorage,
    SQLAlchemyTransaction,
)
from tempo_toolkit.infrastructure.identity import (
    KeycloakAuthorizedUserFinder,
    KeycloakIdentityProvider,
)
from tempo_toolkit.infrastructure.object_storage import S3ObjectStorage
from tempo_toolkit.infrastructure.time import SystemUTCTimer

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
    cacher = provide(RedisCache, provides=Cache)

    # Services
    current_user_service = provide(CurrentUserService)
    upload_service = provide(UploadService)
    outbox_service = provide(OutboxService)

    # ports
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)
    object_storage = provide(S3ObjectStorage, provides=ObjectStorage)
    outbox_storage = provide(SQLAlchemyOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    create_upload = provide(CreateUpload)
    complete_upload = provide(CompleteUpload)
    delete_upload = provide(DeleteUpload)
    healthcheck = provide(Healthcheck)
