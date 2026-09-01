from uuid import UUID

from pydantic import BaseModel

from tempo_toolkit.application.auth import CurrentUserService

from app.core.common.entities.similarity import Similarity
from app.core.common.enums.collections import Collections
from app.core.queries.ports.feature_reader import FeatureReader


class GetSimilarTracksResponse(BaseModel):
    similar_tracks: list[Similarity]


class GetSimilarTracks:
    def __init__(
        self,
        feature_reader: FeatureReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._feature_reader = feature_reader
        self._current_user_service = current_user_service

    async def __call__(self, upload_id: UUID) -> GetSimilarTracksResponse:
        await self._current_user_service.get_current_user(["tempo:etc"])
        similar_points = await self._feature_reader.get_similar(
            Collections.TRACK_FEATURES, id=upload_id
        )
        return GetSimilarTracksResponse(similar_tracks=similar_points)
