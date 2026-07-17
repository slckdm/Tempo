"""Service healthcheck command."""

from botocore.exceptions import ClientError

from tempo_toolkit.infrastructure.object_storage import S3Client, S3Settings

_HEALTHCHECK_KEY = ".tempo-healthcheck"
_MISSING_OBJECT_CODES = frozenset({"404", "NoSuchKey"})


class HealthTrouble(Exception):
    """Raised when a service dependency is unavailable."""


class Healthcheck:
    """Check whether the streaming service dependencies are available."""

    def __init__(self, s3_client: S3Client, s3_settings: S3Settings) -> None:
        """Initialize the command."""
        self._s3_client = s3_client
        self._s3_settings = s3_settings

    async def __call__(self) -> None:
        """Check the object-storage connection and bucket access."""
        try:
            stored_object = await self._s3_client.get_object(
                bucket=self._s3_settings.BUCKET,
                key=_HEALTHCHECK_KEY,
            )
        except ClientError as exception:
            error_code = exception.response.get("Error", {}).get("Code")
            if error_code in _MISSING_OBJECT_CODES:
                return
            raise HealthTrouble from exception
        except Exception as exception:
            raise HealthTrouble from exception

        stored_object.body.close()
