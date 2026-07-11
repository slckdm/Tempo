"""S3 Dishka provider."""

from dishka import Provider, Scope, provide

from .s3 import S3Client
from .settings import S3Settings


class S3Provider(Provider):
    """Provide an application-scoped S3 client."""

    scope = Scope.APP

    @provide
    def get_client(self, config: S3Settings) -> S3Client:
        """Create an S3 client."""
        return S3Client(
            region_name=config.REGION_NAME,
            url=config.URL,
            access_key_id=config.ACCESS_KEY,
            secret_access_key=config.SECRET_KEY,
        )
