from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from server.infrastructure.database.base import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    session_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    character_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    current_region: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    current_scene: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    save_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    faction_reputations: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    unlocked_nodes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    completed_milestones: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    narrative_flags: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
