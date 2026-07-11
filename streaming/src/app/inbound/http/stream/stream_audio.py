"""Module: create upload endpoint."""

from fastapi import Request
from fastapi.responses import StreamingResponse

from dishka.integrations.fastapi import FromDishka, inject

from tempo_toolkit.contracts.uploads import UploadURN

from app.core.queries.stream import Stream


@inject
async def stream_audio(
    request: Request, id: UploadURN, interactor: FromDishka[Stream]
) -> StreamingResponse:
    """Create file upload."""
    stream_data = await interactor(id, request.headers.get("range"))
    headers = {"Accept-Ranges": "bytes", "Content-Length": str(stream_data.content_length)}
    if stream_data.content_range:
        headers.update({"Content-Range": str(stream_data.content_range)})
    return StreamingResponse(
        content=stream_data.chunks,
        status_code=206 if stream_data.content_range else 200,
        media_type=stream_data.content_type,
        headers=headers
    )
