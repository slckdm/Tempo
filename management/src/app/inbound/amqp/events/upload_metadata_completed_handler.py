from dishka_faststream import FromDishka, inject

from tempo_toolkit.contracts.events import MetadataReadyEvent

from app.core.commands.finish_upload import FinishUpload
from app.core.common.exceptions import StatusUpdateFlowError


@inject
async def upload_metadata_completed_handler(
    payload: MetadataReadyEvent, handler: FromDishka[FinishUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return
