import logging

from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage

logger = logging.getLogger(__name__)


class RemoveTrackFromPlaylists:

    def __init__(
        self,
        playlist_track_storage: PlaylistTrackStorage,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._playlist_track_storage = playlist_track_storage
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, track_id: UploadURN) -> None:
        logger.info(f"Removing track {track_id} from playlists")

        await self._playlist_track_storage.delete_all(track_id)
        await self._flusher.flush()
        await self._transaction.commit()
