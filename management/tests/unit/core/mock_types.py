from datetime import datetime
from typing import Protocol
from unittest.mock import AsyncMock


class IdentityProviderMock:
    get_current_user_id: AsyncMock


class AuthorizedUserFinderMock:
    get_by_id: AsyncMock


class UTCTimerMock:

    @property
    def now(self) -> datetime:
        return datetime.now()


class FlusherMock(Protocol):
    flush: AsyncMock


class TransactionMock(Protocol):
    commit: AsyncMock
    rollback: AsyncMock


class UploadStorageMock(Protocol):
    add: AsyncMock
    get_by_id: AsyncMock
    delete: AsyncMock


class OutboxStorageMock(Protocol):
    add: AsyncMock
    get_unpublished: AsyncMock
    mark_as_published: AsyncMock


class ObjectStorageMock(Protocol):
    make_object_upload_url: AsyncMock
    get_object: AsyncMock
    put_object: AsyncMock
    delete_object: AsyncMock
