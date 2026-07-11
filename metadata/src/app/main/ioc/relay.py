
from dishka import Provider, Scope, provide

from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.outbox.adapters.rabbitmq_outbox_message_publisher import (
    FastStreamOutboxMessagePublisher,
)
from toolkit.outbox.adapters.sqla_outbox_storage import SQLAOutboxStorage
from toolkit.outbox.ports.outbox_message_publisher import OutboxMessagePublisher
from toolkit.outbox.ports.outbox_storage import OutboxStorage

from app.core.commands.publish_outbox_messages import PublishOutboxMessages


class RelayProvider(Provider):
    scope = Scope.REQUEST

    event_publisher = provide(FastStreamOutboxMessagePublisher, provides=OutboxMessagePublisher)
    transaction = provide(SQLATransaction, provides=Transaction)
    outbox_storage = provide(SQLAOutboxStorage, provides=OutboxStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    publish_outbox = provide(PublishOutboxMessages)
