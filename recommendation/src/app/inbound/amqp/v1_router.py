from faststream.rabbit import RabbitRouter

from .events.router import make_event_router


def make_v1_router() -> RabbitRouter:
    router = RabbitRouter()
    router.include_routers(
        make_event_router()
    )
    return router
