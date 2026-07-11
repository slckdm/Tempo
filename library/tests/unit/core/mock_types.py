from typing import Protocol
from unittest.mock import AsyncMock


class IdentityProviderMock:
    get_current_user_id: AsyncMock


class AuthorizedUserFinderMock:
    get_by_id: AsyncMock


class FlusherMock(Protocol):
    flush: AsyncMock


class TransactionMock(Protocol):
    commit: AsyncMock
    rollback: AsyncMock


class FavoriteStorageMock(Protocol):
    get: AsyncMock
    get_by_user_and_track_id: AsyncMock
    add: AsyncMock
    remove: AsyncMock
    remove_all: AsyncMock
    get_list: AsyncMock


class PlaylistStorageMock(Protocol):
    get: AsyncMock
    add: AsyncMock
    delete: AsyncMock
    get_list: AsyncMock


class PlaylistTrackStorageMock(Protocol):
    get: AsyncMock
    add: AsyncMock
    delete: AsyncMock
    delete_all: AsyncMock
    get_list: AsyncMock


class FavoriteReaderMock(Protocol):
    get_list: AsyncMock


class PlaylistReaderMock(Protocol):
    get_by_id: AsyncMock
    get_list: AsyncMock


class TrackReaderMock(Protocol):
    get_list: AsyncMock
