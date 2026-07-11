from http import HTTPStatus

from fastapi import APIRouter

from tempo_toolkit.infrastructure.web import jsend as response

from .stream_audio import stream_audio
from .stream_cover import stream_cover


def make_stream_router() -> APIRouter:
    router = APIRouter(prefix="/stream")
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
    router.add_api_route(
        path="/{id}",
        endpoint=stream_audio,
        methods=["GET"],
        responses={**common_responses},
    )
    router.add_api_route(
        path="/{id}/cover",
        endpoint=stream_cover,
        methods=["GET"],
        responses={**common_responses},
    )

    return router
