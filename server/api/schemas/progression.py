from enum import Enum

from pydantic import BaseModel


class NodeState(str, Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    UNLOCKED = "unlocked"


class ProgressionNodeResponse(BaseModel):
    id: str
    name: str
    tier: int
    min_demon_level: int
    narrative_milestone: str
    mana_source: str
    description: str
    effects: dict
    state: NodeState


class ProgressionDomainResponse(BaseModel):
    id: str
    name: str
    primary_archetype: str
    nodes: list[ProgressionNodeResponse]


class UnlockNodeRequest(BaseModel):
    node_id: str


class UnlockNodeResponse(BaseModel):
    node_id: str
    unlocked_nodes: list[str]
