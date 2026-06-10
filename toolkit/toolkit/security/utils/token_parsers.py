"""Module: Token Data Parser Utilities."""

from ..models import ServiceAccount, User


def get_user_data_from_token(payload: dict) -> User:
    """Parse token data into `User` object."""
    return User(
        id=payload["sub"],
        first_name=payload["given_name"],
        last_name=payload["family_name"],
        username=payload["preferred_username"],
        email=payload["email"],
    )


def get_service_account_data_from_token(payload: dict) -> ServiceAccount:
    """Parse token data into `ServiceAccount` object."""
    return ServiceAccount(
        client_id=payload["client_id"],
        preferred_username=payload["preferred_username"],
    )
