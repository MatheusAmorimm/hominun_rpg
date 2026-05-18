from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from server.infrastructure.database.base import Base


class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    race: Mapped[str] = mapped_column(String(30), nullable=False)
    archetype: Mapped[str] = mapped_column(String(30), nullable=False)
    origin: Mapped[str] = mapped_column(String(30), nullable=False)
    current_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    current_mana: Mapped[int] = mapped_column(Integer, nullable=False)
    gold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    save_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    base_stats: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    derived_stats: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    narrative_flags: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    active_demon_ids: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
