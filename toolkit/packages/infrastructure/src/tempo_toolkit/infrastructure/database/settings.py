"""PostgreSQL and SQLAlchemy settings."""

from pydantic import BaseModel, PostgresDsn


class PostgresSettings(BaseModel):
    """PostgreSQL connection settings."""

    HOST: str
    PORT: int
    DATABASE: str
    USERNAME: str
    PASSWORD: str

    @property
    def dsn(self) -> str:
        """Return the SQLAlchemy asyncpg DSN."""
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
    """SQLAlchemy engine settings."""

    ECHO: bool = False
    ECHO_POOL: bool = False
    POOL_SIZE: int = 15
    MAX_OVERFLOW: int = 0
