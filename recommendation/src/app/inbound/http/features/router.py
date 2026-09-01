"""Module: uploads endpoint router."""

from http import HTTPStatus

from fastapi import APIRouter

from tempo_toolkit.infrastructure.web import jsend as response

from .get_similar_features import get_similar_tracks


def make_features_router() -> APIRouter:
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
        HTTPStatus.UNPROCESSABLE_CONTENT: {
            "model": response.ValidationErrorResponse,
            "description": "Validation error",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            "model": response.InternalServerErrorResponse,
            "description": "Internal server error",
        },
    }
    router = APIRouter(prefix="/uploads", tags=["Uploads"])

    router.add_api_route(
        "/{upload_id}",
        get_similar_tracks,
        methods=["GET"],
        responses={
            **common_responses,
            HTTPStatus.NOT_FOUND: {
                "model": response.NotFoundResponse,
                "description": "Upload not found",
            },
        },
    )

    return router
