from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .stream import stream_audio
from .stream_cover import stream_cover


def make_stream_router() -> APIRouter:
    router = APIRouter(prefix="/stream")
    router.add_api_route(
        path="/{id}", endpoint=stream_audio, response_class=StreamingResponse, methods=["GET"]
    )
    router.add_api_route(
        path="/{id}/cover", endpoint=stream_cover, response_class=StreamingResponse, methods=["GET"]
    )

    return router
