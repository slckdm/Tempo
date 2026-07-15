from dishka import FromDishka
from dishka_faststream import inject

from tempo_toolkit.application.errors import NotFound, ObjectStorageError
from tempo_toolkit.contracts.events import UploadCompletedEvent

from app.core.commands.fail_metadata import FailMetadata
from app.core.commands.process_track_metadata import ProcessTrackMetadata
from app.core.common.exceptions import MetadataAlreadyProcessed, TagParseError
from app.outbound.exceptions import MetadataParserError


@inject
async def process_metadata(
    payload: UploadCompletedEvent,
    interactor: FromDishka[ProcessTrackMetadata],
    fail_handler: FromDishka[FailMetadata],
) -> None:
    try:
        await interactor(payload)
    except MetadataAlreadyProcessed:
        return
    except (NotFound, TagParseError, MetadataParserError, ObjectStorageError) as perm_exc:
        await fail_handler(payload, perm_exc)
