import pytest

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.transaction import Transaction
from toolkit.common.services.current_user_service import CurrentUserService

from app.core.commands.create_playlist import (
    CreatePlaylist,
    CreatePlaylistRequest,
)
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.types import PlaylistID
from app.core.models.playlist import Playlist
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist_id,
    create_playlist_service,
    create_user,
)


def make_create_playlist_command(
    current_user_service: CurrentUserService,
    playlist_storage: PlaylistStorage,
    playlist_service: PlaylistService,
    transaction: Transaction,
    flusher: Flusher,
) -> CreatePlaylist:
    return CreatePlaylist(
        current_user_service=current_user_service,
        playlist_storage=playlist_storage,
        playlist_service=playlist_service,
        transaction=transaction,
        flusher=flusher,
    )


def assign_playlist_id(playlist_id: PlaylistID):
    async def wrap(playlist: Playlist) -> None:
        playlist.id = playlist_id

    return wrap


@pytest.mark.asyncio
async def test_create_playlist_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    playlist_id = create_playlist_id()
    user = create_user()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.add.side_effect = assign_playlist_id(playlist_id)
    command = make_create_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_service=create_playlist_service(),
        transaction=transaction,
        flusher=flusher,
    )

    response = await command(CreatePlaylistRequest(name="Daily Rotation"))

    assert response.id == playlist_id
    assert response.user_id == user.id
    assert response.name == "Daily Rotation"
    added = playlist_storage.add.call_args.args[0]
    assert added.user_id == user.id
    assert added.name == "Daily Rotation"
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
