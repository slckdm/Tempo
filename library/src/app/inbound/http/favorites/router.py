from http import HTTPStatus

from fastapi import APIRouter

from toolkit.service import response

from .add_favorite import add_favorite
from .get_favorites import get_favorites
from .remove_favorite import remove_favorite


def make_favorites_router() -> APIRouter:
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
    router = APIRouter(prefix="/favorites")
    router.add_api_route(
        methods=["GET"],
        path="/",
        endpoint=get_favorites,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["POST"],
        path="/",
        endpoint=add_favorite,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["DELETE"],
        path="/{favorite_id}",
        endpoint=remove_favorite,
        responses={**common_responses},
    )

    return router
