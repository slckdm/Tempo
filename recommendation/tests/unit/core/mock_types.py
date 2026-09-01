from datetime import UTC, datetime
from typing import Protocol
from unittest.mock import AsyncMock

FROZEN_NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)


class IdentityProviderMock:
    get_current_user_id: AsyncMock


class AuthorizedUserFinderMock:
    get_by_id: AsyncMock


class UTCTimerMock:
    @property
    def now(self) -> datetime:
        return FROZEN_NOW


class TransactionMock(Protocol):
    commit: AsyncMock
    rollback: AsyncMock


class FeatureStorageMock(Protocol):
    save: AsyncMock
    delete: AsyncMock


class FeatureReaderMock(Protocol):
    get_similar: AsyncMock


class ObjectStorageMock(Protocol):
    get_object: AsyncMock
    put_object: AsyncMock
    delete_object: AsyncMock


class OutboxStorageMock(Protocol):
    add: AsyncMock
    get_unpublished: AsyncMock
    mark_as_published: AsyncMock


class OutboxMessagePublisherMock(Protocol):
    publish: AsyncMock
