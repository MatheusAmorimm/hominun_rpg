from dataclasses import dataclass, field
from typing import Any

from server.domain.value_objects.region_type import DangerLevel, RegionType


@dataclass(frozen=True)
class Region:
    id: str
    name: str
    type: RegionType
    danger_level: DangerLevel
    lore: str
    available_in_acts: frozenset[int]
    connected_region_ids: frozenset[str]
    narrative_flags_required: dict[str, Any]
    special_properties: dict[str, Any] = field(default_factory=dict)

    def is_accessible_in_act(self, act: int) -> bool:
        return not self.available_in_acts or act in self.available_in_acts

    def is_accessible_with_flags(self, player_flags: dict[str, Any]) -> bool:
        return all(
            player_flags.get(key) == value
            for key, value in self.narrative_flags_required.items()
        )

    def is_ether(self) -> bool:
        return self.type == RegionType.ETHER

    def requires_survival_item(self) -> bool:
        return bool(self.special_properties.get("toxic_atmosphere"))

    def survival_item_id(self) -> str | None:
        return self.special_properties.get("survival_item")

    def is_procedural(self) -> bool:
        return bool(self.special_properties.get("procedural"))

    def connects_to(self, region_id: str) -> bool:
        return region_id in self.connected_region_ids
