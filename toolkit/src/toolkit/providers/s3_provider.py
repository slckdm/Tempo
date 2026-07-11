
from dishka import Provider, Scope, provide

from toolkit.config.settings import S3Settings
from toolkit.s3 import S3Client


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def get_client(self, config: S3Settings) -> S3Client:
        return S3Client(
            region_name=config.REGION_NAME,
            url=config.URL,
            access_key_id=config.ACCESS_KEY,
            secret_access_key=config.SECRET_KEY,
        )
