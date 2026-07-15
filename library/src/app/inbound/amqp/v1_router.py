from faststream.rabbit import RabbitRouter

from .events.router import make_events_router


def make_v1_router() -> RabbitRouter:
    router = RabbitRouter()
    router.include_routers(make_events_router())

    return router
