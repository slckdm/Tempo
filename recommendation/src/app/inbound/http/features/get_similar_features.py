"""Module: get similar tracks endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.queries.get_similar_tracks import GetSimilarTracks, GetSimilarTracksResponse


@inject
async def get_similar_tracks(
    upload_id: UploadURN, interactor: FromDishka[GetSimilarTracks]
) -> JSendSuccessfulResponse[GetSimilarTracksResponse]:
    """Get similar tracks."""
    tracks = await interactor(upload_id.id)
    return JSendSuccessfulResponse(data=tracks)
