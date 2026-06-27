"""Module: Public Key Normalization Utility."""


def normalize_public_key(public_key: str | None) -> str:
    """Format JWK as public key.

    Args:
        public_key (str | None, optional): JWK.

    Returns:
        str: Formatted public key or empty string if JWK is `None`.
    """
    if public_key is None:
        return ""
    return f"-----BEGIN PUBLIC KEY-----\n {public_key} \n-----END PUBLIC KEY-----"
