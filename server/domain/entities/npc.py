from dataclasses import dataclass, field
from typing import Any

from server.domain.value_objects.npc_type import NpcAlignment, NpcRole, NpcStatus
from server.domain.value_objects.race_type import RaceType


@dataclass(frozen=True)
class Npc:
    id: str
    name: str
    race: RaceType
    roles: frozenset[NpcRole]
    alignment: NpcAlignment
    status: NpcStatus
    lore: str
    title: str | None = None
    family_id: str | None = None
    is_rival: bool = False
    faction_ids: tuple[str, ...] = field(default_factory=tuple)
    demon_species_ids: tuple[str, ...] = field(default_factory=tuple)
    army_name: str | None = None
    available_in_acts: frozenset[int] = field(default_factory=frozenset)
    region_ids: tuple[str, ...] = field(default_factory=tuple)
    narrative_flags: dict[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        if self.title:
            return f"{self.title} {self.name}"
        return self.name

    def is_summoner(self) -> bool:
        return NpcRole.SUMMONER in self.roles

    def has_army(self) -> bool:
        return self.army_name is not None

    def is_alive(self) -> bool:
        return self.status == NpcStatus.ALIVE

    def belongs_to_faction(self, faction_id: str) -> bool:
        return faction_id in self.faction_ids

    def is_available_in_act(self, act: int) -> bool:
        return not self.available_in_acts or act in self.available_in_acts
