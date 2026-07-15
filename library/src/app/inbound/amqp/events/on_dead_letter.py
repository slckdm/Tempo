import logging

from faststream.rabbit import RabbitMessage


async def on_dead_letter(msg: RabbitMessage) -> None:
    logging.warning("dead-lettered: %r", msg.body)
