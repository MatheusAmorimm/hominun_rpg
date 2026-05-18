from dataclasses import dataclass, field
from typing import Any

_DEFAULT_FACTION_REPUTATIONS = {
    "triumvirate": 0,
    "inquisition": 0,
    "pinkertons": 0,
    "orc_shamans": 0,
    "elven_allies": 0,
}


@dataclass
class SessionState:
    session_id: str
    player_id: str
    narrative_flags: dict[str, Any] = field(default_factory=dict)
    current_region: str = ""
    current_scene: str = ""
    save_version: int = 1
    faction_reputations: dict[str, int] = field(
        default_factory=lambda: dict(_DEFAULT_FACTION_REPUTATIONS)
    )
    unlocked_nodes: list[str] = field(default_factory=list)
    completed_milestones: list[str] = field(default_factory=list)
