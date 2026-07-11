import pytest

from tempo_toolkit.application.persistence import Flusher, Transaction

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from tests.unit.core.factories import create_upload_urn


def make_remove_track_from_favorites_command(
    favorite_storage: FavoriteStorage,
    transaction: Transaction,
    flusher: Flusher,
) -> RemoveTrackFromFavorites:
    return RemoveTrackFromFavorites(
        favorite_storage=favorite_storage,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_remove_track_from_favorites_success(
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    track_id = create_upload_urn()
    command = make_remove_track_from_favorites_command(
        favorite_storage=favorite_storage,
        transaction=transaction,
        flusher=flusher,
    )

    await command(track_id)

    favorite_storage.remove_all.assert_called_once_with(track_id)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
