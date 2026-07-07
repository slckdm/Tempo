from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from .settings import (
    AppSettings,
    KeycloakSettings,
    LoggingSettings,
    PostgresSettings,
    RedisSettings,
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


class KeycloakEnvConfig(BaseSettings, KeycloakSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="KEYCLOAK_")


class AppEnvConfig(BaseSettings, AppSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="APP_")


class SQLAlchemyEnvConfig(BaseSettings, SQLAlchemySettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="SQLA_")


class LoggingEnvConfig(BaseSettings, LoggingSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="LOGGING_")


class RedisEnvConfig(BaseSettings, RedisSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="REDIS_")


def load_app_settings() -> AppSettings:
    return _load_settings(AppEnvConfig)


def load_postgres_settings() -> PostgresSettings:
    return _load_settings(PostgresEnvConfig)


def load_keycloak_settings() -> KeycloakSettings:
    return _load_settings(KeycloakEnvConfig)


def load_sqlalchemy_settings() -> SQLAlchemySettings:
    return _load_settings(SQLAlchemyEnvConfig)


def load_logging_settings() -> LoggingSettings:
    return _load_settings(LoggingEnvConfig)


def load_redis_settings() -> RedisSettings:
    return _load_settings(RedisEnvConfig)
