from typing import cast
from unittest.mock import create_autospec

import pytest

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    FlusherMock,
    IdentityProviderMock,
    ObjectStorageMock,
    OutboxStorageMock,
    TransactionMock,
    UploadStorageMock,
    UTCTimerMock,
)


@pytest.fixture
def identity_provider() -> IdentityProvider:
    return IdentityProviderMock()


@pytest.fixture
def authorized_user_finder() -> AuthorizedUserFinder:
    return AuthorizedUserFinderMock()


@pytest.fixture
def utc_timer() -> UTCTimer:
    return UTCTimerMock()


@pytest.fixture
def flusher() -> Flusher:
    return cast(FlusherMock, create_autospec(Flusher, instance=True))


@pytest.fixture
def transaction() -> Transaction:
    return cast(TransactionMock, create_autospec(Transaction, instance=True))


@pytest.fixture
def upload_storage() -> UploadStorage:
    return cast(UploadStorageMock, create_autospec(UploadStorage, instance=True))


@pytest.fixture
def outbox_storage() -> OutboxStorage:
    return cast(OutboxStorageMock, create_autospec(OutboxStorage, instance=True))


@pytest.fixture
def object_storage() -> ObjectStorage:
    return cast(ObjectStorageMock, create_autospec(ObjectStorage, instance=True))
