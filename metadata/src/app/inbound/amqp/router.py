from faststream.rabbit import RabbitRouter

from .events.router import router as events_router
from .metadata.router import router as metadata_router

router = RabbitRouter()

router.include_routers(events_router, metadata_router)
