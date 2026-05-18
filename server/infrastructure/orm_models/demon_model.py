from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from server.infrastructure.database.base import Base


class DemonModel(Base):
    __tablename__ = "demons"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    character_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    species_id: Mapped[str] = mapped_column(String(60), nullable=False)
    given_name: Mapped[str] = mapped_column(String(60), nullable=False)
    temperament: Mapped[str] = mapped_column(String(30), nullable=False)
    affinity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    current_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    current_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
