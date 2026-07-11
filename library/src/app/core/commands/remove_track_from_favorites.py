import logging

from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.commands.ports.favorite_storage import FavoriteStorage

logger = logging.getLogger(__name__)


class RemoveTrackFromFavorites:
    def __init__(
        self,
        favorite_storage: FavoriteStorage,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._favorite_storage = favorite_storage
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, track_id: UploadURN) -> None:
        logger.info(f"Removing track {track_id} from favorites")

        await self._favorite_storage.remove_all(track_id)
        await self._flusher.flush()
        await self._transaction.commit()
