from uuid import UUID

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.common.entities.similarity import Similarity
from app.core.common.enums.collections import Collections
from app.core.queries.ports.feature_reader import FeatureReader
from app.outbound.exceptions import FeatureNotFoundError


class QdrantFeatureReader(FeatureReader):
    def __init__(self, qdrant_client: AsyncQdrantClient) -> None:
        self._qdrant_client = qdrant_client

    async def get_similar(self, collection: Collections, id: UUID) -> list[Similarity]:
        try:
            response = await self._qdrant_client.query_points(collection, query=str(id))
        except UnexpectedResponse as qdrant_error:
            if qdrant_error.status_code == 404:
                raise FeatureNotFoundError from qdrant_error
            raise qdrant_error

        return [Similarity(point_id=point.id, score=point.score) for point in response.points]
