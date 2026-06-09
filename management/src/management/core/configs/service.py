"""Module: Service configuration."""

from dataclasses import dataclass
from os import environ as env


@dataclass
class ServiceConfig:
    """Service configuration object."""

    name: str = env["SERVICE_NAME"]
    port: int = int(env["SERVICE_PORT"])
