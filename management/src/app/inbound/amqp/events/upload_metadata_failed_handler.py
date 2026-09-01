from dishka_faststream import FromDishka, inject

from tempo_toolkit.contracts.events import MetadataFailedEvent

from app.core.commands.fail_upload import FailUpload
from app.core.common.exceptions import StatusUpdateFlowError


@inject
async def upload_metadata_failed_handler(
    payload: MetadataFailedEvent, handler: FromDishka[FailUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return
