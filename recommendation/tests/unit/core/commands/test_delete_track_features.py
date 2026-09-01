import pytest

from app.core.commands.delete_track_features import DeleteSongFeatures
from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.common.enums.collections import Collections
from tests.unit.core.factories import create_metadata_deleted_event


@pytest.mark.asyncio
async def test_delete_track_features_success(feature_storage: FeatureStorage) -> None:
    event = create_metadata_deleted_event()

    await DeleteSongFeatures(feature_storage)(event)

    feature_storage.delete.assert_awaited_once_with(
        Collections.TRACK_FEATURES,
        str(event.upload_id.id),
    )
