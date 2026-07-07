
from fastapi import APIRouter

from app.inbound.http.favorites.router import make_favorites_router
from app.inbound.http.playlists.router import make_playlists_router


def make_v1_router() -> APIRouter:
    v1_router = APIRouter(prefix="/library")
    v1_router.include_router(make_favorites_router(), tags=["Favorites"])
    v1_router.include_router(make_playlists_router(), tags=["Playlists"])

    return v1_router
