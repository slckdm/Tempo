"""Shared logging configuration."""

from enum import StrEnum

from pydantic import BaseModel

FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


class LoggingLevel(StrEnum):
    """Supported application logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingSettings(BaseModel):
    """Application logging settings."""

    LEVEL: LoggingLevel = LoggingLevel.INFO
