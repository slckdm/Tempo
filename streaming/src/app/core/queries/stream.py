from dataclasses import dataclass
from io import IOBase
from typing import Any, Generator, Iterator

from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import NotFound, ObjectStorageError
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.uploads import UploadURN

_DEFAULT_CHUNK_SIZE = 256 * 1024


def _iter_chunks(bytes: IOBase, chunk_size=_DEFAULT_CHUNK_SIZE) -> Generator[Any, Any, None]:
    try:
        while chunk := bytes.read(chunk_size):
            yield chunk
    finally:
        bytes.close()


@dataclass(frozen=True)
class StreamData:
    content_type: str
    content_range: str | None
    content_length: int
    chunks: Iterator[bytes]


class Stream:
    def __init__(
        self,
        object_storage: ObjectStorage,
        current_user_service: CurrentUserService,
    ) -> None:
        self._object_storage = object_storage
        self._current_user_service = current_user_service

    async def __call__(
        self, id: UploadURN, range_header: str | None, cover: bool = False
    ) -> StreamData:
        await self._current_user_service.get_current_user(["tempo:streaming"])

        params = {"Range": range_header} if range_header else {}
        key = ("covers/" if cover else "") + str(id)
        try:
            object = await self._object_storage.get_object(key, **params)
        except ObjectStorageError as storage_err:
            raise NotFound from storage_err

        return StreamData(
            content_type=object.content_type,
            content_range=object.content_range,
            content_length=object.content_length,
            chunks=_iter_chunks(object.body),
        )
