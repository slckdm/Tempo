"""Module: uploads endpoint router."""

from http import HTTPStatus

from fastapi import APIRouter

from toolkit.service import response

from app.core.schemas.response import CompleteUploadResponseBody, CreateUploadResponseBody

from .complete_upload import complete_upload
from .create_upload import create_upload


def make_uploads_router() -> APIRouter:
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
        "",
        create_upload,
        methods=["POST"],
        response_model=response.JSendSuccessfulResponse[CreateUploadResponseBody],
        responses={
            **common_responses,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE: {
                "model": response.UnsupportedMediaTypeResponse,
                "description": "Unsupported media type error",
            },
        },
    )
    router.add_api_route(
        "/{upload_id}/complete",
        complete_upload,
        methods=["POST"],
        response_model=response.JSendSuccessfulResponse[CompleteUploadResponseBody],
        responses={**common_responses},
    )

    return router
