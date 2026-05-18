from dataclasses import dataclass


@dataclass(frozen=True)
class CombatRules:
    base_hit_chance: float = 0.80
    critical_multiplier: float = 1.5
    affinity_damage_bonus_per_point: float = 0.01
    max_affinity: int = 100
    flee_base_chance: float = 0.40
