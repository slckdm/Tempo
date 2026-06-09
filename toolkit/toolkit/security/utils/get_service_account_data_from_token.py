from ..models import ServiceAccount

def get_service_account_data_from_token(payload: dict) -> ServiceAccount:
    return ServiceAccount(
        client_id=payload["client_id"],
        preferred_username=payload["preferred_username"],
    )
