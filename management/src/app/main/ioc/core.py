from dishka import Provider, Scope, provide

from app.core.commands.create_upload import CreateUpload
from app.core.ports.flusher import Flusher
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.sqla_upload_storage import SQLAUploadStorage
from app.outbound.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from app.outbound.keycloak_identity_provider import KeycloakIdentityProvider
from app.services.current_user_service import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from app.services.upload_service import UploadService


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)

    # Services
    current_user_service = provide(CurrentUserService)
    upload_service = provide(UploadService)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    upload_storage = provide(SQLAUploadStorage, provides=UploadStorage)

    # commands
    create_upload = provide(CreateUpload)
