"""Module: uploads endpoint router."""

from fastapi import APIRouter

from toolkit.response import JSendErrorResponse, JSendFailResponse, JSendSuccessfulResponse

from management.schemas.response import CreateUploadResponseBody

from .complete_upload import complete_upload
from .create_upload import create_upload

uploads_router = APIRouter(prefix="/uploads", tags=["Uploads"])
common_responses = {
    400: {"model": JSendFailResponse, "description": "Bad request"},
    422: {"model": JSendErrorResponse, "description": "Validation error"},
}

uploads_router.add_api_route(
    "/create",
    create_upload,
    methods=["POST"],
    response_model=JSendSuccessfulResponse[CreateUploadResponseBody],
    responses={**common_responses},
)

# uploads_router.add_api_route(
#     "/complete",
#     complete_upload,
#     methods=["POST"],
#     response_model=JSendSuccessfulResponse[CreateUploadResponseBody],
#     responses={**common_responses}
# )
