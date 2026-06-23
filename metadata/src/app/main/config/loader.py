from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from toolkit.messaging.settings import RabbitMQSettings

from .settings import (
    AppSettings,
    KeycloakSettings,
    PostgresSettings,
    S3Settings,
    SQLAlchemySettings,
)

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[4]
_ENV_FILE: Final[Path] = BASE_DIR.joinpath(".env")

_DEFAULT_CONFIG_DICT: Final[SettingsConfigDict] = SettingsConfigDict(
    env_file=_ENV_FILE, extra="ignore"
)


def _load_settings[E: BaseSettings](env_cls: type[E]) -> E:
    return env_cls()


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


def load_app_settings() -> AppSettings:
    return _load_settings(AppEnvConfig)


def load_postgres_settings() -> PostgresSettings:
    return _load_settings(PostgresEnvConfig)


def load_keycloak_settings() -> KeycloakSettings:
    return _load_settings(KeycloakEnvConfig)


def load_s3_settings() -> S3Settings:
    return _load_settings(S3EnvConfig)


def load_sqlalchemy_settings() -> SQLAlchemySettings:
    return _load_settings(SQLAlchemyEnvConfig)


def load_rabbitmq_settings() -> RabbitMQSettings:
    return _load_settings(RabbitMQEnvConfig)
