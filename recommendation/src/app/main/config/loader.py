from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from tempo_toolkit.infrastructure.cache import RedisSettings
from tempo_toolkit.infrastructure.configuration import load_settings
from tempo_toolkit.infrastructure.database import PostgresSettings, SQLAlchemySettings
from tempo_toolkit.infrastructure.identity import KeycloakSettings
from tempo_toolkit.infrastructure.logging import LoggingSettings
from tempo_toolkit.infrastructure.messaging import RabbitMQSettings
from tempo_toolkit.infrastructure.object_storage import S3Settings
from tempo_toolkit.infrastructure.web import AppSettings

from app.main.config.settings import QdrantSettings

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[4]
_ENV_FILE: Final[Path] = BASE_DIR.joinpath(".env")

print(_ENV_FILE)
_DEFAULT_CONFIG_DICT: Final[SettingsConfigDict] = SettingsConfigDict(
    env_file=_ENV_FILE, extra="ignore"
)


class PostgresEnvConfig(BaseSettings, PostgresSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="POSTGRES_")


class S3EnvConfig(BaseSettings, S3Settings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="S3_")


class KeycloakEnvConfig(BaseSettings, KeycloakSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="KEYCLOAK_")


class AppEnvConfig(BaseSettings, AppSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="APP_")


class SQLAlchemyEnvConfig(BaseSettings, SQLAlchemySettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="SQLA_")


class RabbitMQEnvConfig(BaseSettings, RabbitMQSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="RMQ_")


class LoggingEnvConfig(BaseSettings, LoggingSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="LOGGING_")


class RedisEnvConfig(BaseSettings, RedisSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="REDIS_")


class QdrantEnvConfig(BaseSettings, QdrantSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="QDRANT_")


def load_app_settings() -> AppSettings:
    return load_settings(AppEnvConfig)


def load_postgres_settings() -> PostgresSettings:
    return load_settings(PostgresEnvConfig)


def load_keycloak_settings() -> KeycloakSettings:
    return load_settings(KeycloakEnvConfig)


def load_s3_settings() -> S3Settings:
    return load_settings(S3EnvConfig)


def load_sqlalchemy_settings() -> SQLAlchemySettings:
    return load_settings(SQLAlchemyEnvConfig)


def load_rabbitmq_settings() -> RabbitMQSettings:
    return load_settings(RabbitMQEnvConfig)


def load_logging_settings() -> LoggingSettings:
    return load_settings(LoggingEnvConfig)


def load_redis_settings() -> RedisSettings:
    return load_settings(RedisEnvConfig)


def load_qdrant_settings() -> QdrantSettings:
    return load_settings(QdrantEnvConfig)
