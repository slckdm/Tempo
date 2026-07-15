from fastapi.routing import APIRouter

from .healthcheck.router import make_healthcheck_router
from .uploads.router import make_uploads_router


def make_v1_router() -> APIRouter:
    router = APIRouter()

    router.include_router(make_healthcheck_router())
    router.include_router(make_uploads_router())

    return router
