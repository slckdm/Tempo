"""JWT decoding and principal parsing."""

from jwt import decode

from tempo_toolkit.application.auth import ServiceAccount, User


def decode_token(token: str, public_key: str, audience: list[str]) -> dict:
    """Decode and verify an RS256 token."""
    return decode(
        jwt=token,
        key=public_key,
        algorithms=["RS256"],
        audience=audience or [],
        options={"verify_exp": True, "verify_aud": True},
    )


def normalize_public_key(public_key: str | None) -> str:
    """Wrap a Keycloak realm key in PEM markers."""
    if public_key is None:
        return ""
    return f"-----BEGIN PUBLIC KEY-----\n {public_key} \n-----END PUBLIC KEY-----"


def get_user_data_from_token(payload: dict) -> User:
    """Parse user claims."""
    return User(
        id=payload["sub"],
        first_name=payload["given_name"],
        last_name=payload["family_name"],
        username=payload["preferred_username"],
        email=payload["email"],
    )


def get_service_account_data_from_token(payload: dict) -> ServiceAccount:
    """Parse service-account claims."""
    return ServiceAccount(
        client_id=payload["client_id"],
        preferred_username=payload["preferred_username"],
    )
