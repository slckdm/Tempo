from typing import cast
from unittest.mock import create_autospec

import pytest

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.queries.ports.favorite_reader import FavoriteReader
from app.core.queries.ports.playlist_reader import PlaylistReader
from app.core.queries.ports.tracks_reader import TrackReader
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    FavoriteReaderMock,
    FavoriteStorageMock,
    FlusherMock,
    IdentityProviderMock,
    PlaylistReaderMock,
    PlaylistStorageMock,
    PlaylistTrackStorageMock,
    TrackReaderMock,
    TransactionMock,
)


@pytest.fixture
def identity_provider() -> IdentityProvider:
    return cast(IdentityProviderMock, create_autospec(IdentityProvider, instance=True))


@pytest.fixture
def authorized_user_finder() -> AuthorizedUserFinder:
    return cast(AuthorizedUserFinderMock, create_autospec(AuthorizedUserFinder, instance=True))


@pytest.fixture
def flusher() -> Flusher:
    return cast(FlusherMock, create_autospec(Flusher, instance=True))


@pytest.fixture
def transaction() -> Transaction:
    return cast(TransactionMock, create_autospec(Transaction, instance=True))


@pytest.fixture
def favorite_storage() -> FavoriteStorage:
    return cast(FavoriteStorageMock, create_autospec(FavoriteStorage, instance=True))


@pytest.fixture
def playlist_storage() -> PlaylistStorage:
    return cast(PlaylistStorageMock, create_autospec(PlaylistStorage, instance=True))


@pytest.fixture
def playlist_track_storage() -> PlaylistTrackStorage:
    return cast(
        PlaylistTrackStorageMock,
        create_autospec(PlaylistTrackStorage, instance=True),
    )


@pytest.fixture
def favorite_reader() -> FavoriteReader:
    return cast(FavoriteReaderMock, create_autospec(FavoriteReader, instance=True))


@pytest.fixture
def playlist_reader() -> PlaylistReader:
    return cast(PlaylistReaderMock, create_autospec(PlaylistReader, instance=True))


@pytest.fixture
def track_reader() -> TrackReader:
    return cast(TrackReaderMock, create_autospec(TrackReader, instance=True))
