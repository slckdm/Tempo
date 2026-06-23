from datetime import datetime
from uuid import UUID

from sqlalchemy import types as orm
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OutboxMessage(Base):
    __tablename__ = "outbox_messages"

    id: Mapped[int] = mapped_column(orm.Integer, primary_key=True, autoincrement=True)
    aggregate_type: Mapped[str] = mapped_column(orm.String)
    aggregate_id: Mapped[UUID] = mapped_column(orm.UUID)
    event_type: Mapped[str] = mapped_column(orm.String)
    payload: Mapped[dict] = mapped_column(orm.JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(orm.DateTime(timezone=True))
    published_at: Mapped[datetime | None] = mapped_column(
        orm.DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"aggregate_type={self.aggregate_type}, "
            f"aggregate_id={self.aggregate_id}, "
            f"event_type={self.event_type})"
        )
