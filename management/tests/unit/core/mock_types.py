import random
from datetime import datetime
from typing import Protocol
from unittest.mock import AsyncMock

from toolkit.entities import ServiceAccount, User
from toolkit.types_ import UserID

from .factories import create_user


class IdentityProviderMock:
    # get_current_user_id: AsyncMock

    async def get_current_user_id(self) -> UserID:
        return random.choice(AuthorizedUserFinderMock._users).id


class AuthorizedUserFinderMock:
    # get_by_id: AsyncMock
    _users = [create_user(), create_user(), create_user()]
    _users_map = {user.id: user for user in _users}

    async def get_by_id(self, id: UserID) -> User | ServiceAccount | None:
        return self._users_map.get(id)


class UTCTimerMock:

    @property
    def now(self) -> datetime:
        return datetime.now()


class FlusherMock(Protocol):
    flush: AsyncMock


class TransactionMock(Protocol):
    commit: AsyncMock


class UploadStorageMock(Protocol):
    add: AsyncMock
    get_by_id: AsyncMock


class OutboxStorageMock(Protocol):
    add: AsyncMock
    get_unpublished: AsyncMock
    mark_as_published: AsyncMock


class ObjectStorageMock(Protocol):
    make_object_upload_url: AsyncMock
    get_object: AsyncMock
    put_object: AsyncMock
