from pydantic import BaseModel

class ServiceAccount(BaseModel):
    client_id: str
    preferred_username: str
