from pydantic import BaseModel


class QdrantSettings(BaseModel):
    HOST: str
    PORT: int
