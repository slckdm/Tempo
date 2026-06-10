"""Module: uploads endpoint router."""

from http import HTTPStatus

from fastapi import APIRouter

from toolkit.service.response import (
    BadRequestResponse,
    ForbiddenResponse,
    InternalServerErrorResponse,
    JSendSuccessfulResponse,
    UnsupportedMediaTypeResponse,
    ValidationErrorResponse,
)

from management.schemas.response import CreateUploadResponseBody

from .complete_upload import complete_upload
from .create_upload import create_upload

uploads_router = APIRouter(prefix="/uploads", tags=["Uploads"])
common_responses = {
    HTTPStatus.BAD_REQUEST: {"model": BadRequestResponse, "description": "Bad request"},
    HTTPStatus.FORBIDDEN: {"model": ForbiddenResponse, "description": "Forbidden"},
    HTTPStatus.UNPROCESSABLE_CONTENT: {
        "model": ValidationErrorResponse,
        "description": "Validation error",
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        "model": InternalServerErrorResponse,
        "description": "Internal server error",
    },
}

uploads_router.add_api_route(
    "/create",
    create_upload,
    methods=["POST"],
    response_model=JSendSuccessfulResponse[CreateUploadResponseBody],
    responses={
        **common_responses,
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE: {
            "model": UnsupportedMediaTypeResponse,
            "description": "Unsupported media type error",
        },
    },
)

# uploads_router.add_api_route(
#     "/complete",
#     complete_upload,
#     methods=["POST"],
#     response_model=JSendSuccessfulResponse[CreateUploadResponseBody],
#     responses={**common_responses}
# )
