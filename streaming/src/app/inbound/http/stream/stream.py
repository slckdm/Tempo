"""Module: create upload endpoint."""

from fastapi import Request
from fastapi.responses import StreamingResponse

from dishka.integrations.fastapi import FromDishka, inject

from app.core.commands.stream_audio import StreamAudio
from app.core.common.types_ import UploadURNType


@inject
async def stream_audio(
    request: Request, id: UploadURNType, interactor: FromDishka[StreamAudio]
) -> StreamingResponse:
    """Create file upload."""
    audio = await interactor.execute(id, request.headers.get("range"))
    headers = {"Accept-Ranges": "bytes", "Content-Length": str(audio.content_length)}
    if audio.content_range:
        headers.update({"Content-Range": str(audio.content_range)})

    return StreamingResponse(
        audio.chunks, status_code=audio.status_code, media_type=audio.content_type, headers=headers
    )
