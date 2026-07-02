from pydantic import BaseModel

from toolkit.logging import LoggingLevel


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
