import pytest

from toolkit.service.exceptions import NotFound

from app.core.commands.delete_playlist import DeletePlaylist
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.types import PlaylistID
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist,
    create_playlist_id,
    create_playlist_service,
    create_user,
)


def make_delete_playlist_command(
    current_user_service: CurrentUserService,
    playlist_storage: PlaylistStorage,
    playlist_service: PlaylistService,
    transaction: Transaction,
    flusher: Flusher,
) -> DeletePlaylist:
    return DeletePlaylist(
        current_user_service=current_user_service,
        playlist_storage=playlist_storage,
        playlist_service=playlist_service,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_delete_playlist_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    playlist = create_playlist(user_id=user.id)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = playlist
    command = make_delete_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_service=create_playlist_service(),
        transaction=transaction,
        flusher=flusher,
    )

    await command(playlist.id)

    playlist_storage.get.assert_called_once_with(user.id, playlist.id)
    playlist_storage.delete.assert_called_once_with(playlist)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_playlist_not_found(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    playlist_id = create_playlist_id()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = None
    command = make_delete_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_service=create_playlist_service(),
        transaction=transaction,
        flusher=flusher,
    )

    with pytest.raises(NotFound):
        await command(playlist_id)

    playlist_storage.delete.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
