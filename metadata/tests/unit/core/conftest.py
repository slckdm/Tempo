from typing import cast
from unittest.mock import create_autospec

import pytest

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.metadata_parser import MetadataParser
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_message_publisher import OutboxMessagePublisher
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.queries.ports.metadata_reader import MetadataReader
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    FlusherMock,
    IdentityProviderMock,
    MetadataParserMock,
    MetadataReaderMock,
    MetadataStorageMock,
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
def flusher() -> Flusher:
    return cast(FlusherMock, create_autospec(Flusher, instance=True))


@pytest.fixture
def transaction() -> Transaction:
    return cast(TransactionMock, create_autospec(Transaction, instance=True))


@pytest.fixture
def metadata_storage() -> MetadataStorage:
    return cast(MetadataStorageMock, create_autospec(MetadataStorage, instance=True))


@pytest.fixture
def outbox_storage() -> OutboxStorage:
    return cast(OutboxStorageMock, create_autospec(OutboxStorage, instance=True))


@pytest.fixture
def object_storage() -> ObjectStorage:
    return cast(ObjectStorageMock, create_autospec(ObjectStorage, instance=True))


@pytest.fixture
def metadata_parser() -> MetadataParser:
    return cast(MetadataParserMock, create_autospec(MetadataParser, instance=True))


@pytest.fixture
def outbox_message_publisher() -> OutboxMessagePublisher:
    return cast(
        OutboxMessagePublisherMock, create_autospec(OutboxMessagePublisher, instance=True)
    )


@pytest.fixture
def metadata_reader() -> MetadataReader:
    return cast(MetadataReaderMock, create_autospec(MetadataReader, instance=True))
