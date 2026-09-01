import asyncio
import io
import logging

import librosa
import numpy as np
from numpy._typing._array_like import NDArray

from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.events import MetadataReadyEvent

from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.common.entities.collection_metadata import CollectionMetadata
from app.core.common.enums.collections import Collections


class SaveSongFeatures:
    def __init__(
        self,
        feature_storage: FeatureStorage,
        object_storage: ObjectStorage,
    ) -> None:
        self._feature_storage = feature_storage
        self._object_storage = object_storage

    async def __call__(self, payload: MetadataReadyEvent) -> None:
        logging.debug("Processing features from track=%s", payload.upload_id)
        object_data = await self._object_storage.get_object(str(payload.upload_id))
        content = io.BytesIO(await asyncio.to_thread(object_data.body.read))
        object_data.body.close()
        logging.debug("Extracting features from track=%s", payload.upload_id)
        features = await asyncio.to_thread(self._extract_song_features, content)
        await self._feature_storage.save(
            Collections.TRACK_FEATURES,
            str(payload.upload_id.id),
            features.tolist(),
            metadata=CollectionMetadata(
                title=payload.title,
                artist=payload.artist,
                album=payload.album,
                genre=payload.genre,
                year=payload.year,
                content_type=payload.content_type,
            ),
        )
        logging.debug("Features saved for track=%s", payload.upload_id)

    def _extract_song_features(self, track: io.BytesIO) -> NDArray[np.float64]:
        y, sr = librosa.load(track)

        rms = librosa.feature.rms(y=y)
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        rms_mean = np.mean(rms, axis=1)
        mfccs_mean = np.mean(mfccs, axis=1)
        chroma_mean = np.mean(chroma, axis=1)
        if isinstance(tempo, np.ndarray):
            tempo_mean = np.mean(tempo, keepdims=True)
        else:
            tempo_mean = np.array([tempo])

        return np.concatenate([mfccs_mean, chroma_mean, tempo_mean, rms_mean])
