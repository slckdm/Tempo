"""Module: Token User Data Decoder Utility."""

from jwt import decode

from toolkit.entities import ServiceAccount, User

from .token_parsers import get_service_account_data_from_token, get_user_data_from_token


def decode_token(token: str, public_key: str) -> User | ServiceAccount:
    """Decode token data into `User` object.

    Args:
        token (str): Client token.
        public_key (str): Public key for decoding.

    Returns:
        User | ServiceAccount: Decoded user or service account data from token.
    """
    validation_options = {
        "options": {
            "verify_exp": True,
            "verify_aud": False,
        },
        "audience": [],
    }
    payload = decode(
        jwt=token,
        key=public_key,
        algorithms=["RS256"],
        verify=False,
        **validation_options,
    )

    parser = get_service_account_data_from_token
    if "client_id" not in payload:
        parser = get_user_data_from_token

    return parser(payload)
