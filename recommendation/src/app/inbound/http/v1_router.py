from fastapi.routing import APIRouter

from .features.router import make_features_router
from .healthcheck.router import make_healthcheck_router


def make_v1_router() -> APIRouter:
    router = APIRouter()

    router.include_router(make_healthcheck_router())
    router.include_router(make_features_router())

    return router
