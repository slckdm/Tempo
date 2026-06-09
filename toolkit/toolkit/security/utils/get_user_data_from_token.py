from ..models import User

def get_user_data_from_token(payload: dict) -> User:
    return User(
        first_name=payload["given_name"],
        last_name=payload["family_name"],
        username=payload["preferred_username"],
        email=payload["email"],
    )
