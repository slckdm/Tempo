from dishka import Provider, Scope
from starlette.concurrency import run_in_threadpool

from toolkit.s3.s3_client import S3Client

from app.core.commands.stream_audio import AudioObject
from app.core.common.exceptions import ObjectNotFound
from app.core.ports.audio_storage import AudioStorage
from app.main.config.settings import S3Settings


class S3AudioStorage(Provider, AudioStorage):
    scope = Scope.APP

    def __init__(self, s3_client: S3Client, s3_config: S3Settings) -> None:
        self._s3_client = s3_client
        self._s3_config = s3_config

    async def get(self, key: str, range_header: str | None) -> AudioObject:
        kwargs = {}
        if range_header:
            kwargs["Range"] = range_header
        data = await run_in_threadpool(
            self._s3_client.get_object, bucket_name=self._s3_config.BUCKET, key=key, **kwargs
        )

        if not data:
            raise ObjectNotFound
        content_range = data.get("ContentRange")
        return AudioObject(
            206 if data.get("ContentRange") else 200,
            data.get("ContentType", "application/octet-stream"),
            int(content_range) if content_range else None,
            data["ContentLength"],
            data["Body"].iter_chunks(chunk_size=256 * 1024),
        )
