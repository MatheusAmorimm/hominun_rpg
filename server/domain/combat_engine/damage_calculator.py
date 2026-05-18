from server.domain.combat_engine.affinity_modifier import affinity_damage_multiplier
from server.domain.combat_engine.combat_rules import CombatRules


def calculate_damage(
    base_damage: int,
    affinity: int,
    is_critical: bool,
    rules: CombatRules,
) -> int:
    damage = base_damage * affinity_damage_multiplier(affinity, rules)
    if is_critical:
        damage *= rules.critical_multiplier
    return max(1, int(damage))
