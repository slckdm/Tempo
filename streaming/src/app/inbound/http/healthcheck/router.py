"""Healthcheck endpoint router."""

from http import HTTPStatus

from fastapi import APIRouter

from tempo_toolkit.infrastructure.web import jsend as response

from .healthcheck import healthcheck


def make_healthcheck_router() -> APIRouter:
    """Create the healthcheck endpoint router."""
    router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])
    router.add_api_route(
        "/",
        healthcheck,
        methods=["GET"],
        responses={
            HTTPStatus.INTERNAL_SERVER_ERROR: {
                "model": response.InternalServerErrorResponse,
                "description": "Internal server error",
            }
        },
    )
    return router
