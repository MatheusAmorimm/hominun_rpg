from pydantic import BaseModel


class NpcSummaryResponse(BaseModel):
    id: str
    name: str
    full_name: str
    race: str
    roles: list[str]
    alignment: str
    status: str
    is_rival: bool


class NpcResponse(BaseModel):
    id: str
    name: str
    full_name: str
    title: str | None
    race: str
    roles: list[str]
    alignment: str
    status: str
    is_rival: bool
    family_id: str | None
    faction_ids: list[str]
    region_ids: list[str]
    available_in_acts: list[int]
    lore: str
    narrative_flags: dict
