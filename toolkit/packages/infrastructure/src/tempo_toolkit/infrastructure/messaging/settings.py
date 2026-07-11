"""RabbitMQ settings."""

from pydantic import BaseModel


class RabbitMQSettings(BaseModel):
    """RabbitMQ connection settings."""

    HOST: str | None = None
    PORT: int | None = None
    VHOST: str | None = None
    APP_ID: str | None = None
    USER: str
    PASSWORD: str
