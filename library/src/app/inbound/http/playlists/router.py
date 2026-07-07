from http import HTTPStatus

from fastapi import APIRouter

from toolkit.service import response

from .add_track_to_playlist import add_track_to_playlist
from .create_playlist import create_playlist
from .delete_playlist import delete_playlist
from .get_playlist import get_playlist
from .get_playlist_tracks import get_playlist_tracks
from .get_playlists import get_playlists
from .remove_track_from_playlist import remove_track_from_playlist


def make_playlists_router() -> APIRouter:
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
    router = APIRouter(prefix="/playlists")

    router.add_api_route(
        methods=["POST"],
        path="/",
        endpoint=create_playlist,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["GET"],
        path="/",
        endpoint=get_playlists,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["GET"],
        path="/{playlist_id}",
        endpoint=get_playlist,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["DELETE"],
        path="/{playlist_id}",
        endpoint=delete_playlist,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["GET"],
        path="/{playlist_id}/tracks",
        endpoint=get_playlist_tracks,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["POST"],
        path="/{playlist_id}/tracks",
        endpoint=add_track_to_playlist,
        responses={**common_responses},
    )
    router.add_api_route(
        methods=["DELETE"],
        path="/{playlist_id}/tracks",
        endpoint=remove_track_from_playlist,
        responses={**common_responses},
    )

    return router
