import asyncio
from io import BytesIO

from tinytag import TinyTag, TinyTagException

from app.core.commands.ports.metadata_parser import MetadataParser
from app.core.common.entities.metadata import Cover, Metadata
from app.outbound.exceptions import MetadataParserError


class TinyTagMetadataParser(MetadataParser):
    async def read(self, bytes: BytesIO) -> Metadata:
        try:
            data = await asyncio.to_thread(
                TinyTag.get, file_obj=bytes, tags=True, duration=True, image=True
            )
            image = data.images.any
            metadata = Metadata(
                album=data.album,
                albumartist=data.albumartist,
                artist=data.artist,
                bitrate=data.bitrate,
                channels=data.channels,
                comment=data.comment,
                composer=data.composer,
                disc=data.disc,
                disc_total=data.disc_total,
                duration=data.duration,
                genre=data.genre,
                samplerate=data.samplerate,
                title=data.title,
                track=data.track,
                track_total=data.track_total,
                year=data.year,
                cover=Cover(data=image.data, mime_type=image.mime_type) if image else None,
            )
            return metadata
        except TinyTagException as tt_exc:
            raise MetadataParserError from tt_exc
