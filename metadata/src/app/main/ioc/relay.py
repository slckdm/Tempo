
from dishka import Provider, Scope, provide

from app.core.commands.ports.outbox_message_publisher import OutboxMessagePublisher
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.utc_timer import UTCTimer
from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.outbound.adapters.rabbitmq_outbox_message_publisher import (
    FastStreamOutboxMessagePublisher,
)
from app.outbound.adapters.sqla_outbox_storage import SQLAOutboxStorage
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.system_utc_timer import SystemUTCTimer


class RelayProvider(Provider):
    scope = Scope.REQUEST

    event_publisher = provide(FastStreamOutboxMessagePublisher, provides=OutboxMessagePublisher)
    transaction = provide(SQLATransaction, provides=Transaction)
    outbox_storage = provide(SQLAOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    publish_outbox = provide(PublishOutboxMessages)
