from typing import cast
from unittest.mock import create_autospec

import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider
from tempo_toolkit.application.outbox import OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.application.time import UTCTimer

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.ports.metadata_proxy import MetadataProxy
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    FlusherMock,
    IdentityProviderMock,
    MetadataProxyMock,
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


@pytest.fixture
def metadata_proxy() -> MetadataProxy:
    return cast(MetadataProxyMock, create_autospec(MetadataProxy, instance=True))
