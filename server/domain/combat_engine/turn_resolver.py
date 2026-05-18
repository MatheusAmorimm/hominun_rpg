from dataclasses import dataclass
from enum import Enum


class TurnAction(str, Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    CAST = "cast"
    ORDER_DEMON = "order_demon"
    FLEE = "flee"
    INTIMIDATE = "intimidate"


@dataclass
class TurnResult:
    action: TurnAction
    damage_dealt: int
    damage_received: int
    affinity_delta: int
    narrative_tag: str
    is_critical: bool = False
    fled: bool = False
