from typing import cast
from unittest.mock import create_autospec

import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider
from tempo_toolkit.application.outbox import OutboxMessagePublisher, OutboxStorage
from tempo_toolkit.application.persistence import Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.application.time import UTCTimer

from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.queries.ports.feature_reader import FeatureReader
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    FeatureReaderMock,
    FeatureStorageMock,
    IdentityProviderMock,
    ObjectStorageMock,
    OutboxMessagePublisherMock,
    OutboxStorageMock,
    TransactionMock,
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
def transaction() -> Transaction:
    return cast(TransactionMock, create_autospec(Transaction, instance=True))


@pytest.fixture
def feature_storage() -> FeatureStorage:
    return cast(FeatureStorageMock, create_autospec(FeatureStorage, instance=True))


@pytest.fixture
def feature_reader() -> FeatureReader:
    return cast(FeatureReaderMock, create_autospec(FeatureReader, instance=True))


@pytest.fixture
def object_storage() -> ObjectStorage:
    return cast(ObjectStorageMock, create_autospec(ObjectStorage, instance=True))


@pytest.fixture
def outbox_storage() -> OutboxStorage:
    return cast(OutboxStorageMock, create_autospec(OutboxStorage, instance=True))


@pytest.fixture
def outbox_message_publisher() -> OutboxMessagePublisher:
    return cast(
        OutboxMessagePublisherMock,
        create_autospec(OutboxMessagePublisher, instance=True),
    )
