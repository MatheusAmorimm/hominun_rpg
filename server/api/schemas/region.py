from pydantic import BaseModel


class RegionSummaryResponse(BaseModel):
    id: str
    name: str
    type: str
    danger_level: str
    available_in_acts: list[int]
    connected_region_ids: list[str]


class RegionResponse(BaseModel):
    id: str
    name: str
    type: str
    danger_level: str
    requires_flags: dict
    survival_item: str | None
    procedural: bool
    special_properties: list[str]
    lore: str
    connected_region_ids: list[str]
    available_in_acts: list[int]


class MovePlayerRequest(BaseModel):
    region_id: str


class MovePlayerResponse(BaseModel):
    session_id: str
    current_region: str
    current_scene: str
