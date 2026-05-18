from dataclasses import dataclass, field
from typing import Any

from server.domain.value_objects.faction_type import FactionAlignment, FactionType, ReputationStatus


@dataclass(frozen=True)
class ReputationThresholds:
    hostile: int
    unfriendly: int
    neutral: int
    friendly: int
    honored: int


@dataclass(frozen=True)
class Faction:
    id: str
    name: str
    type: FactionType
    alignment: FactionAlignment
    goals: tuple[str, ...]
    leader_npc_id: str
    member_npc_ids: tuple[str, ...]
    rival_faction_ids: tuple[str, ...]
    allied_faction_ids: tuple[str, ...]
    reputation_thresholds: ReputationThresholds
    lore: str
    available_in_acts: frozenset[int] = field(default_factory=frozenset)
    narrative_flags: dict[str, Any] = field(default_factory=dict)

    def reputation_status(self, score: int) -> ReputationStatus:
        t = self.reputation_thresholds
        if score <= t.hostile:
            return ReputationStatus.HOSTILE
        if score <= t.unfriendly:
            return ReputationStatus.UNFRIENDLY
        if score <= t.neutral:
            return ReputationStatus.NEUTRAL
        if score <= t.friendly:
            return ReputationStatus.FRIENDLY
        return ReputationStatus.HONORED

    def is_rival_of(self, faction_id: str) -> bool:
        return faction_id in self.rival_faction_ids

    def is_allied_with(self, faction_id: str) -> bool:
        return faction_id in self.allied_faction_ids

    def has_member(self, npc_id: str) -> bool:
        return npc_id in self.member_npc_ids

    def is_available_in_act(self, act: int) -> bool:
        return not self.available_in_acts or act in self.available_in_acts
