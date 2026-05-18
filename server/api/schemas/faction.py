from pydantic import BaseModel, Field


class FactionSummaryResponse(BaseModel):
    id: str
    name: str
    type: str
    alignment: str
    leader_npc_id: str
    available_in_acts: list[int]


class ReputationEntry(BaseModel):
    score: int
    status: str


class ReputationsResponse(BaseModel):
    reputations: dict[str, ReputationEntry]


class UpdateReputationRequest(BaseModel):
    faction_id: str
    delta: int = Field(..., ge=-100, le=100)


class UpdateReputationResponse(BaseModel):
    faction_id: str
    score: int
    status: str
