import json
from pathlib import Path

from server.domain.entities.npc import Npc
from server.domain.ports.npc_repository import NpcRepository
from server.domain.value_objects.npc_type import NpcAlignment, NpcRole, NpcStatus
from server.domain.value_objects.race_type import RaceType

_NPCS_FILE = Path(__file__).parents[4] / "data" / "npcs" / "npcs.json"


def _parse_npc(data: dict) -> Npc:
    return Npc(
        id=data["id"],
        name=data["name"],
        race=RaceType(data["race"]),
        roles=frozenset(NpcRole(r) for r in data["roles"]),
        alignment=NpcAlignment(data["alignment"]),
        status=NpcStatus(data["status"]),
        lore=data["lore"],
        title=data.get("title"),
        family_id=data.get("family_id"),
        is_rival=data.get("is_rival", False),
        faction_ids=tuple(data.get("faction_ids", [])),
        demon_species_ids=tuple(data.get("demon_species_ids", [])),
        army_name=data.get("army_name"),
        available_in_acts=frozenset(data.get("available_in_acts", [])),
        region_ids=tuple(data.get("region_ids", [])),
        narrative_flags=data.get("narrative_flags", {}),
    )


class JsonNpcRepository(NpcRepository):
    def __init__(self) -> None:
        with open(_NPCS_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        self._npcs: dict[str, Npc] = {n["id"]: _parse_npc(n) for n in raw}

    async def get_all(self) -> list[Npc]:
        return list(self._npcs.values())

    async def get_by_id(self, npc_id: str) -> Npc | None:
        return self._npcs.get(npc_id)

    async def get_by_region(self, region_id: str) -> list[Npc]:
        return [n for n in self._npcs.values() if region_id in n.region_ids]
