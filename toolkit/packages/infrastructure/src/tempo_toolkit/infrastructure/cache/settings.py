"""Redis settings."""

from pydantic import BaseModel


class RedisSettings(BaseModel):
    """Redis connection settings."""

    HOST: str
    PORT: int
    DB: str
    PASSWORD: str
