from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldState:
    world_id: str
    active_sessions: list[str] = field(default_factory=list)
    global_flags: dict[str, Any] = field(default_factory=dict)
    act: int = 1
