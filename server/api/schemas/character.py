from uuid import UUID

from pydantic import BaseModel, Field


class BonusStatDistribution(BaseModel):
    str_: int = Field(0, ge=0)
    dex: int = Field(0, ge=0)
    con: int = Field(0, ge=0)
    int_: int = Field(0, ge=0)
    wis: int = Field(0, ge=0)
    cha: int = Field(0, ge=0)


class CreateCharacterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=60)
    race: str
    archetype: str
    origin: str
    bonus_stat_distribution: BonusStatDistribution = Field(default_factory=BonusStatDistribution)


class BaseStatsResponse(BaseModel):
    str_: int
    dex: int
    con: int
    int_: int
    wis: int
    cha: int


class DerivedStatsResponse(BaseModel):
    hp: int
    mana: int
    initiative: int
    ether_resistance: int


class CharacterResponse(BaseModel):
    id: UUID
    name: str
    race: str
    archetype: str
    origin: str
    base_stats: BaseStatsResponse
    derived_stats: DerivedStatsResponse
    current_hp: int
    current_mana: int
    gold: int
    narrative_flags: dict
    active_demon_ids: list[str]
