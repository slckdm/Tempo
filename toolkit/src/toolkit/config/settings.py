from pydantic import BaseModel, PostgresDsn

from toolkit.logging import LoggingLevel


class PostgresSettings(BaseModel):
    HOST: str
    PORT: int
    DATABASE: str
    USERNAME: str
    PASSWORD: str

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.USERNAME,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                path=self.DATABASE,
            )
        )


class SQLAlchemySettings(BaseModel):
    ECHO: bool = False
    ECHO_POOL: bool = False
    POOL_SIZE: int = 15
    MAX_OVERFLOW: int = 0


class KeycloakSettings(BaseModel):
    URL: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    @property
    def token_url(self) -> str:
        return f"{self.URL}/realms/{self.REALM}/protocol/openid-connect/token"


class S3Settings(BaseModel):
    URL: str
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET: str
    REGION_NAME: str = "us-east-1"


class AppSettings(BaseModel):
    NAME: str
    HOST: str
    PORT: int
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str]


class LoggingSettings(BaseModel):
    LEVEL: LoggingLevel = LoggingLevel.INFO


class RedisSettings(BaseModel):
    HOST: str
    PORT: int
    DB: str
    PASSWORD: str


class RabbitMQSettings(BaseModel):
    HOST: str | None = None
    PORT: int | None = None
    VHOST: str | None = None
    APP_ID: str | None = None
    USER: str
    PASSWORD: str
