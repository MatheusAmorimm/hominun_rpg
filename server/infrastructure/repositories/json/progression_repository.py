import json
from pathlib import Path

from server.domain.entities.progression import ProgressionDomain, ProgressionNode
from server.domain.ports.progression_repository import ProgressionRepository
from server.domain.value_objects.progression_type import ManaSource, NodeTier, ProgressionDomainId

_PROGRESSION_FILE = Path(__file__).parents[4] / "data" / "progression" / "progression_tree.json"


def _parse_node(data: dict) -> ProgressionNode:
    return ProgressionNode(
        id=data["id"],
        name=data["name"],
        tier=NodeTier(data["tier"]),
        min_demon_level=data["min_demon_level"],
        narrative_milestone=data["narrative_milestone"],
        mana_source=ManaSource(data["mana_source"]),
        description=data["description"],
        effects=data.get("effects", {}),
    )


def _parse_domain(data: dict) -> ProgressionDomain:
    return ProgressionDomain(
        id=ProgressionDomainId(data["id"]),
        name=data["name"],
        primary_archetype=data["primary_archetype"],
        nodes=tuple(_parse_node(n) for n in data["nodes"]),
    )


class JsonProgressionRepository(ProgressionRepository):
    def __init__(self) -> None:
        with open(_PROGRESSION_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        self._domains: dict[str, ProgressionDomain] = {d["id"]: _parse_domain(d) for d in raw}

    async def get_all_domains(self) -> list[ProgressionDomain]:
        return list(self._domains.values())

    async def get_domain_by_id(self, domain_id: str) -> ProgressionDomain | None:
        return self._domains.get(domain_id)

    async def get_node_domain(self, node_id: str) -> ProgressionDomain | None:
        for domain in self._domains.values():
            if domain.get_node(node_id):
                return domain
        return None
