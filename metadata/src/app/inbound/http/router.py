from http import HTTPMethod, HTTPStatus

from fastapi import APIRouter

from toolkit.service import response

from app.core.schemas.response import TrackMetadataResponseBody, TracksMetadataResponseBody

from .get_track_metadata import get_track_metadata
from .get_tracks_metadata import get_tracks_metadata


def make_tracks_metadata_router() -> APIRouter:
    common_responses = {
        HTTPStatus.UNAUTHORIZED: {
            "model": response.UnauthorizedResponse,
            "description": "Unauthorized",
        },
        HTTPStatus.BAD_REQUEST: {
            "model": response.BadRequestResponse,
            "description": "Bad request",
        },
        HTTPStatus.FORBIDDEN: {"model": response.ForbiddenResponse, "description": "Forbidden"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            "model": response.InternalServerErrorResponse,
            "description": "Internal server error",
        },
    }

    router = APIRouter(prefix="/metadata")
    router.add_api_route(
        methods=[HTTPMethod.GET],
        path="/{upload_id}",
        endpoint=get_track_metadata,
        response_model=response.JSendSuccessfulResponse[TrackMetadataResponseBody],
        responses={**common_responses}
    )
    router.add_api_route(
        methods=[HTTPMethod.GET],
        path="/",
        endpoint=get_tracks_metadata,
        response_model=response.JSendSuccessfulResponse[TracksMetadataResponseBody],
        responses={**common_responses}
    )

    return router
