from server.domain.combat_engine.combat_rules import CombatRules


def affinity_damage_multiplier(affinity: int, rules: CombatRules) -> float:
    clamped = max(0, min(affinity, rules.max_affinity))
    return 1.0 + clamped * rules.affinity_damage_bonus_per_point
