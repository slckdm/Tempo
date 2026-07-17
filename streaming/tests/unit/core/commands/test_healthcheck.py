import io
from unittest.mock import create_autospec

import pytest
from botocore.exceptions import ClientError

from tempo_toolkit.application.storage import StoredObject
from tempo_toolkit.infrastructure.object_storage import S3Client, S3Settings

from app.core.commands.healthcheck import Healthcheck, HealthTrouble


def create_s3_settings() -> S3Settings:
    return S3Settings(
        URL="http://s3",
        ACCESS_KEY="access-key",
        SECRET_KEY="secret-key",
        BUCKET="tracks",
    )


@pytest.mark.asyncio
async def test_healthcheck_missing_reserved_object_is_healthy() -> None:
    s3_client = create_autospec(S3Client, instance=True)
    s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
        "GetObject",
    )

    await Healthcheck(s3_client, create_s3_settings())()

    s3_client.get_object.assert_awaited_once_with(
        bucket="tracks",
        key=".tempo-healthcheck",
    )


@pytest.mark.asyncio
async def test_healthcheck_closes_existing_reserved_object() -> None:
    s3_client = create_autospec(S3Client, instance=True)
    body = io.BytesIO(b"")
    s3_client.get_object.return_value = StoredObject(
        body=body,
        content_length=0,
        content_type="application/octet-stream",
    )

    await Healthcheck(s3_client, create_s3_settings())()

    assert body.closed


@pytest.mark.asyncio
async def test_healthcheck_storage_failure() -> None:
    s3_client = create_autospec(S3Client, instance=True)
    s3_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "GetObject",
    )

    with pytest.raises(HealthTrouble):
        await Healthcheck(s3_client, create_s3_settings())()
