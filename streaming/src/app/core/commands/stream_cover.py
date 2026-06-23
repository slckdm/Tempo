from dataclasses import dataclass
from io import IOBase
from typing import Any, Generator, Iterator

from toolkit.types.urn import UploadURNType

from app.core.commands.ports.object_storage import ObjectStorage
from app.outbound.ports.identity_provider import IdentityProvider

_DEFAULT_CHUNK_SIZE = 256 * 1024


def _iter_chunks(bytes: IOBase, chunk_size=_DEFAULT_CHUNK_SIZE) -> Generator[Any, Any, None]:
    while True:
        current_chunk = bytes.read(chunk_size)
        if current_chunk == b"":
            break
        yield current_chunk


@dataclass(frozen=True)
class Stream:
    content_type: str
    content_range: int | None
    content_length: int
    chunks: Iterator[bytes]


class StreamCover:

    def __init__(
        self,
        object_storage: ObjectStorage,
        identity: IdentityProvider,
    ) -> None:
        self._object_storage = object_storage
        self._identity = identity

    async def __call__(self, id: UploadURNType, range_header: str | None) -> Stream:
        await self._identity.get_current_user_id()

        object = await self._object_storage.get_object("covers/" + str(id))

        return Stream(
            content_type=object.content_type,
            content_range=object.content_range,
            content_length=object.content_length,
            chunks=_iter_chunks(object.body)
        )
