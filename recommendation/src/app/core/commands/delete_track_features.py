import logging

from tempo_toolkit.contracts.events import MetadataDeletedEvent

from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.common.enums.collections import Collections


class DeleteSongFeatures:
    def __init__(
        self,
        feature_storage: FeatureStorage,
    ) -> None:
        self._feature_storage = feature_storage

    async def __call__(self, payload: MetadataDeletedEvent) -> None:
        logging.debug("Deleting features for track=%s", payload.upload_id)
        await self._feature_storage.delete(
            Collections.TRACK_FEATURES,
            str(payload.upload_id.id),
        )
        logging.debug("Features deleted for track=%s", payload.upload_id)
