import json
from pathlib import Path

from server.domain.entities.faction import Faction, ReputationThresholds
from server.domain.ports.faction_repository import FactionRepository
from server.domain.value_objects.faction_type import FactionAlignment, FactionType

_FACTIONS_FILE = Path(__file__).parents[4] / "data" / "factions" / "factions.json"


def _parse_faction(data: dict) -> Faction:
    t = data["reputation_thresholds"]
    return Faction(
        id=data["id"],
        name=data["name"],
        type=FactionType(data["type"]),
        alignment=FactionAlignment(data["alignment"]),
        goals=tuple(data["goals"]),
        leader_npc_id=data["leader_npc_id"],
        member_npc_ids=tuple(data.get("member_npc_ids", [])),
        rival_faction_ids=tuple(data.get("rival_faction_ids", [])),
        allied_faction_ids=tuple(data.get("allied_faction_ids", [])),
        reputation_thresholds=ReputationThresholds(
            hostile=t["hostile"],
            unfriendly=t["unfriendly"],
            neutral=t["neutral"],
            friendly=t["friendly"],
            honored=t["honored"],
        ),
        lore=data["lore"],
        available_in_acts=frozenset(data.get("available_in_acts", [])),
        narrative_flags=data.get("narrative_flags", {}),
    )


class JsonFactionRepository(FactionRepository):
    def __init__(self) -> None:
        with open(_FACTIONS_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        self._factions: dict[str, Faction] = {f["id"]: _parse_faction(f) for f in raw}

    async def get_all(self) -> list[Faction]:
        return list(self._factions.values())

    async def get_by_id(self, faction_id: str) -> Faction | None:
        return self._factions.get(faction_id)
