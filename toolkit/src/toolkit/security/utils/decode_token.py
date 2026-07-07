"""Module: Token User Data Decoder Utility."""

from jwt import decode


def decode_token(token: str, public_key: str, audience: list[str]) -> dict:
    """Decode token data into `User` object.

    Args:
        token (str): Client token.
        public_key (str): Public key for decoding.
        audience (list[str]): List of valid audiences.

    Returns:
        dict: Decoded token data.
    """
    options = {"verify_exp": True, "verify_aud": True}
    payload = decode(
        jwt=token,
        key=public_key,
        algorithms=["RS256"],
        audience=audience or [],
        options=options,
    )

    return payload
