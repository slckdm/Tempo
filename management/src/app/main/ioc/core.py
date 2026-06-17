from dishka import Provider, Scope, provide

from app.core.commands.complete_upload import CompleteUpload
from app.core.commands.create_upload import CreateUpload
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.outbox_service import OutboxService
from app.core.common.services.upload_service import UploadService
from app.core.ports.flusher import Flusher
from app.core.ports.outbox_storage import OutboxStorage
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage
from app.core.ports.utc_timer import UTCTimer
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_outbox_storage import SQLAOutboxStorage
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage
from app.outbound.adapters.system_utc_timer import SystemUTCTimer
from app.outbound.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.keycloak_identity_provider import KeycloakIdentityProvider
from app.outbound.ports.auth_user_finder import AuthorizedUserFinder
from app.outbound.ports.identity_provider import IdentityProvider


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # Services
    current_user_service = provide(CurrentUserService)
    upload_service = provide(UploadService)
    outbox_service = provide(OutboxService)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)
    outbox_storage = provide(SQLAOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    create_upload = provide(CreateUpload)
    complete_upload = provide(CompleteUpload)
