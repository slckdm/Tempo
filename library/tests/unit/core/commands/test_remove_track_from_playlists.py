import pytest

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists
from tests.unit.core.factories import create_upload_urn


def make_remove_track_from_playlists_command(
    playlist_track_storage: PlaylistTrackStorage,
    transaction: Transaction,
    flusher: Flusher,
) -> RemoveTrackFromPlaylists:
    return RemoveTrackFromPlaylists(
        playlist_track_storage=playlist_track_storage,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_remove_track_from_playlists_success(
    playlist_track_storage: PlaylistTrackStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    track_id = create_upload_urn()
    command = make_remove_track_from_playlists_command(
        playlist_track_storage=playlist_track_storage,
        transaction=transaction,
        flusher=flusher,
    )

    await command(track_id)

    playlist_track_storage.delete_all.assert_called_once_with(track_id)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
