import json
from pathlib import Path

from server.domain.entities.region import Region
from server.domain.ports.region_repository import RegionRepository
from server.domain.value_objects.region_type import DangerLevel, RegionType

_REGIONS_FILE = Path(__file__).parents[4] / "data" / "regions" / "regions.json"


def _parse_region(data: dict) -> Region:
    return Region(
        id=data["id"],
        name=data["name"],
        type=RegionType(data["type"]),
        danger_level=DangerLevel(data["danger_level"]),
        lore=data.get("lore", ""),
        connected_region_ids=frozenset(data.get("connected_regions", [])),
        narrative_flags_required=data.get("narrative_flags_required", {}),
        special_properties=data.get("special_properties", {}),
        available_in_acts=frozenset(data.get("available_in_acts", [])),
    )


class JsonRegionRepository(RegionRepository):
    def __init__(self) -> None:
        with open(_REGIONS_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        self._regions: dict[str, Region] = {r["id"]: _parse_region(r) for r in raw}

    async def get_all(self) -> list[Region]:
        return list(self._regions.values())

    async def get_by_id(self, region_id: str) -> Region | None:
        return self._regions.get(region_id)
