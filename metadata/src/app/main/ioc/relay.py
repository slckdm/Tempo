
from dishka import Provider, Scope, provide

from tempo_toolkit.application.outbox import OutboxMessagePublisher, OutboxStorage
from tempo_toolkit.application.persistence import Transaction
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.database import SQLAlchemyOutboxStorage, SQLAlchemyTransaction
from tempo_toolkit.infrastructure.messaging import (
    FastStreamOutboxMessagePublisher,
)
from tempo_toolkit.infrastructure.time import SystemUTCTimer

from app.core.commands.publish_outbox_messages import PublishOutboxMessages


class RelayProvider(Provider):
    scope = Scope.REQUEST

    event_publisher = provide(FastStreamOutboxMessagePublisher, provides=OutboxMessagePublisher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    outbox_storage = provide(SQLAlchemyOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    publish_outbox = provide(PublishOutboxMessages)
