from typing import cast
from unittest.mock import create_autospec

import pytest
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.outbox.ports.outbox_storage import OutboxStorage

from app.core.commands.ports.upload_storage import UploadStorage
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
    return cast(IdentityProviderMock, create_autospec(IdentityProvider, instance=True))


@pytest.fixture
def authorized_user_finder() -> AuthorizedUserFinder:
    return cast(AuthorizedUserFinderMock, create_autospec(AuthorizedUserFinder, instance=True))


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
