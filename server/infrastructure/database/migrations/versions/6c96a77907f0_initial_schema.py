"""initial_schema

Revision ID: 6c96a77907f0
Revises:
Create Date: 2026-05-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "6c96a77907f0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("nickname", sa.String(60), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "characters",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(60), nullable=False),
        sa.Column("race", sa.String(30), nullable=False),
        sa.Column("archetype", sa.String(30), nullable=False),
        sa.Column("origin", sa.String(30), nullable=False),
        sa.Column("current_hp", sa.Integer, nullable=False),
        sa.Column("current_mana", sa.Integer, nullable=False),
        sa.Column("save_version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("base_stats", JSONB, nullable=False, server_default="{}"),
        sa.Column("derived_stats", JSONB, nullable=False, server_default="{}"),
        sa.Column("narrative_flags", JSONB, nullable=False, server_default="{}"),
        sa.Column("active_demon_ids", JSONB, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_characters_user_id", "characters", ["user_id"])

    op.create_table(
        "sessions",
        sa.Column("session_id", UUID(as_uuid=True), primary_key=True),
        sa.Column("character_id", UUID(as_uuid=True), sa.ForeignKey("characters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("current_region", sa.String(60), nullable=False, server_default=""),
        sa.Column("current_scene", sa.String(60), nullable=False, server_default=""),
        sa.Column("save_version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("faction_reputations", JSONB, nullable=False, server_default="{}"),
        sa.Column("unlocked_nodes", JSONB, nullable=False, server_default="[]"),
        sa.Column("completed_milestones", JSONB, nullable=False, server_default="[]"),
        sa.Column("narrative_flags", JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_sessions_character_id", "sessions", ["character_id"])

    op.create_table(
        "campaign_saves",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", UUID(as_uuid=True), sa.ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slot_name", sa.String(100), nullable=False),
        sa.Column("act", sa.Integer, nullable=False, server_default="1"),
        sa.Column("current_region", sa.String(60), nullable=False, server_default=""),
        sa.Column("state_snapshot", JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_campaign_saves_session_id", "campaign_saves", ["session_id"])
    op.create_index("ix_campaign_saves_user_id", "campaign_saves", ["user_id"])

    op.create_table(
        "demons",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("character_id", UUID(as_uuid=True), sa.ForeignKey("characters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("species_id", sa.String(60), nullable=False),
        sa.Column("given_name", sa.String(60), nullable=False),
        sa.Column("temperament", sa.String(30), nullable=False),
        sa.Column("affinity", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_hp", sa.Integer, nullable=False),
        sa.Column("current_mana", sa.Integer, nullable=False),
        sa.Column("level", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_demons_character_id", "demons", ["character_id"])


def downgrade() -> None:
    op.drop_table("demons")
    op.drop_table("campaign_saves")
    op.drop_table("sessions")
    op.drop_table("characters")
    op.drop_table("users")
