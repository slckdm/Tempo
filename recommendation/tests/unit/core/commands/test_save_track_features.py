import io
from unittest.mock import patch

import numpy as np
import pytest

from tempo_toolkit.application.storage import ObjectStorage

from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.commands.save_track_features import SaveSongFeatures
from app.core.common.entities.collection_metadata import CollectionMetadata
from app.core.common.enums.collections import Collections
from tests.unit.core.factories import create_metadata_ready_event, create_object


@pytest.mark.asyncio
async def test_save_track_features_success(
    feature_storage: FeatureStorage,
    object_storage: ObjectStorage,
) -> None:
    event = create_metadata_ready_event()
    stored_object = create_object()
    expected_features = np.arange(34, dtype=np.float64)
    object_storage.get_object.return_value = stored_object
    command = SaveSongFeatures(feature_storage, object_storage)

    with patch.object(
        command,
        "_extract_song_features",
        return_value=expected_features,
    ) as extract_features:
        await command(event)

    object_storage.get_object.assert_awaited_once_with(str(event.upload_id))
    extract_features.assert_called_once()
    assert stored_object.body.closed
    feature_storage.save.assert_awaited_once_with(
        Collections.TRACK_FEATURES,
        str(event.upload_id.id),
        expected_features.tolist(),
        metadata=CollectionMetadata(
            title=event.title,
            artist=event.artist,
            album=event.album,
            genre=event.genre,
            year=event.year,
            content_type=event.content_type,
        ),
    )


@pytest.mark.parametrize(
    ("tempo", "expected_tempo"),
    [
        (120.0, 120.0),
        (np.array([120.0, 124.0]), 122.0),
    ],
)
def test_extract_track_features(tempo: float | np.ndarray, expected_tempo: float) -> None:
    feature_storage = object()
    object_storage = object()
    command = SaveSongFeatures(feature_storage, object_storage)
    samples = np.array([0.1, 0.2])
    rms = np.array([[1.0, 3.0]])
    mfccs = np.arange(40, dtype=np.float64).reshape(20, 2)
    chroma = np.arange(24, dtype=np.float64).reshape(12, 2)

    with (
        patch(
            "app.core.commands.save_track_features.librosa.load", return_value=(samples, 44_100)
        ),
        patch("app.core.commands.save_track_features.librosa.feature.rms", return_value=rms),
        patch("app.core.commands.save_track_features.librosa.feature.mfcc", return_value=mfccs),
        patch(
            "app.core.commands.save_track_features.librosa.beat.beat_track",
            return_value=(tempo, None),
        ),
        patch(
            "app.core.commands.save_track_features.librosa.feature.chroma_stft",
            return_value=chroma,
        ),
    ):
        result = command._extract_song_features(io.BytesIO(b"audio"))

    expected = np.concatenate(
        [
            np.mean(mfccs, axis=1),
            np.mean(chroma, axis=1),
            np.array([expected_tempo]),
            np.mean(rms, axis=1),
        ]
    )
    np.testing.assert_array_equal(result, expected)
    assert result.shape == (34,)
