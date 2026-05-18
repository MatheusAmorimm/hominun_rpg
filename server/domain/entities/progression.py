from dataclasses import dataclass, field
from typing import Any

from server.domain.value_objects.progression_type import ManaSource, NodeTier, ProgressionDomainId

_ARCHETYPE_PRIMARY_DOMAIN = {
    "pure_summoner": ProgressionDomainId.DEMONIC_BOND,
    "battle_mage": ProgressionDomainId.PERSONAL_COMBAT,
    "ether_explorer": ProgressionDomainId.ETHER_KNOWLEDGE,
}

_ARCHETYPE_LEVEL_DISCOUNT = 3


@dataclass(frozen=True)
class ProgressionNode:
    id: str
    name: str
    tier: NodeTier
    min_demon_level: int
    narrative_milestone: str
    mana_source: ManaSource
    description: str
    effects: dict[str, Any] = field(default_factory=dict)

    def is_unlockable(
        self,
        total_demon_level: int,
        completed_milestones: frozenset[str],
        archetype: str,
        domain_id: ProgressionDomainId,
    ) -> bool:
        effective_level = self._effective_level_requirement(archetype, domain_id)
        return (
            total_demon_level >= effective_level
            and self.narrative_milestone in completed_milestones
        )

    def _effective_level_requirement(self, archetype: str, domain_id: ProgressionDomainId) -> int:
        if _ARCHETYPE_PRIMARY_DOMAIN.get(archetype) == domain_id:
            return max(1, self.min_demon_level - _ARCHETYPE_LEVEL_DISCOUNT)
        return self.min_demon_level


@dataclass(frozen=True)
class ProgressionDomain:
    id: ProgressionDomainId
    name: str
    primary_archetype: str
    nodes: tuple[ProgressionNode, ...]

    def get_node(self, node_id: str) -> ProgressionNode | None:
        return next((n for n in self.nodes if n.id == node_id), None)

    def available_nodes(
        self,
        total_demon_level: int,
        completed_milestones: frozenset[str],
        unlocked_node_ids: frozenset[str],
        archetype: str,
    ) -> tuple[ProgressionNode, ...]:
        return tuple(
            n for n in self.nodes
            if n.id not in unlocked_node_ids
            and n.is_unlockable(total_demon_level, completed_milestones, archetype, self.id)
        )

    def nodes_by_tier(self, tier: NodeTier) -> tuple[ProgressionNode, ...]:
        return tuple(n for n in self.nodes if n.tier == tier)
