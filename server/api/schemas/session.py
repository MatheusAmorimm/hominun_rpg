from uuid import UUID

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    character_id: UUID


class SessionResponse(BaseModel):
    session_id: str
    player_id: str
    current_region: str
    current_scene: str
    faction_reputations: dict[str, int]
    unlocked_nodes: list[str]
    completed_milestones: list[str]
    save_version: int
