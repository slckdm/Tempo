import pytest

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.transaction import Transaction
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.service.exceptions import NotFound

from app.core.commands.add_track_to_playlist import AddTrackToPlaylist
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.services.playlist_track_service import PlaylistTrackService
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist,
    create_playlist_id,
    create_playlist_service,
    create_playlist_track_service,
    create_upload_urn,
    create_user,
)


def make_add_track_to_playlist_command(
    current_user_service: CurrentUserService,
    playlist_storage: PlaylistStorage,
    playlist_track_storage: PlaylistTrackStorage,
    playlist_service: PlaylistService,
    playlist_track_service: PlaylistTrackService,
    transaction: Transaction,
    flusher: Flusher,
) -> AddTrackToPlaylist:
    return AddTrackToPlaylist(
        current_user_service=current_user_service,
        playlist_storage=playlist_storage,
        playlist_track_storage=playlist_track_storage,
        playlist_service=playlist_service,
        playlist_track_service=playlist_track_service,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_add_track_to_playlist_success(
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
    command = make_add_track_to_playlist_command(
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
    added_track, added_playlist = playlist_track_storage.add.call_args.args
    assert added_track.playlist_id == playlist.id
    assert added_track.track_id == str(track_id)
    assert added_playlist is playlist
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_add_track_to_playlist_not_found(
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
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_storage.get.return_value = None
    command = make_add_track_to_playlist_command(
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

    playlist_track_storage.add.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
