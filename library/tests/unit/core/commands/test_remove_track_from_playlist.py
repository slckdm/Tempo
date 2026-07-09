import pytest

from toolkit.service.exceptions import NotFound

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.remove_track_from_playlist import RemoveTrackFromPlaylist
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.services.playlist_track_service import PlaylistTrackService
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist,
    create_playlist_id,
    create_playlist_service,
    create_playlist_track,
    create_playlist_track_service,
    create_upload_urn,
    create_user,
)


def make_remove_track_from_playlist_command(
    current_user_service: CurrentUserService,
    playlist_storage: PlaylistStorage,
    playlist_track_storage: PlaylistTrackStorage,
    playlist_service: PlaylistService,
    playlist_track_service: PlaylistTrackService,
    transaction: Transaction,
    flusher: Flusher,
) -> RemoveTrackFromPlaylist:
    return RemoveTrackFromPlaylist(
        current_user_service=current_user_service,
        playlist_storage=playlist_storage,
        playlist_track_storage=playlist_track_storage,
        playlist_service=playlist_service,
        playlist_track_service=playlist_track_service,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_remove_track_from_playlist_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    playlist_track_storage: PlaylistTrackStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    track_id = create_upload_urn()
    playlist = create_playlist(user_id=user.id)
    playlist_track = create_playlist_track(playlist_id=playlist.id, track_id=track_id)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = playlist
    playlist_track_storage.get.return_value = playlist_track
    command = make_remove_track_from_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_track_storage=playlist_track_storage,
        playlist_service=create_playlist_service(),
        playlist_track_service=create_playlist_track_service(),
        transaction=transaction,
        flusher=flusher,
    )

    await command(playlist.id, track_id)

    playlist_storage.get.assert_called_once_with(user.id, playlist.id)
    playlist_track_storage.get.assert_called_once_with(playlist.id, track_id)
    playlist_track_storage.delete.assert_called_once_with(playlist_track)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_remove_track_from_playlist_missing_playlist(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    playlist_track_storage: PlaylistTrackStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    playlist_id = create_playlist_id()
    track_id = create_upload_urn()
    playlist_track = create_playlist_track(playlist_id=playlist_id, track_id=track_id)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = None
    playlist_track_storage.get.return_value = playlist_track
    command = make_remove_track_from_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_track_storage=playlist_track_storage,
        playlist_service=create_playlist_service(),
        playlist_track_service=create_playlist_track_service(),
        transaction=transaction,
        flusher=flusher,
    )

    with pytest.raises(NotFound):
        await command(playlist_id, track_id)

    playlist_track_storage.delete.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()


@pytest.mark.asyncio
async def test_remove_track_from_playlist_missing_track(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    playlist_storage: PlaylistStorage,
    playlist_track_storage: PlaylistTrackStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    playlist = create_playlist(user_id=user.id)
    track_id = create_upload_urn()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = playlist
    playlist_track_storage.get.return_value = None
    command = make_remove_track_from_playlist_command(
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        playlist_storage=playlist_storage,
        playlist_track_storage=playlist_track_storage,
        playlist_service=create_playlist_service(),
        playlist_track_service=create_playlist_track_service(),
        transaction=transaction,
        flusher=flusher,
    )

    with pytest.raises(NotFound):
        await command(playlist.id, track_id)

    playlist_track_storage.delete.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
