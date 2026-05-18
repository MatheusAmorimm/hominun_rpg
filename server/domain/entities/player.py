from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from server.domain.value_objects.race_type import ArchetypeType, OriginType, RaceType
from server.domain.value_objects.stats import BaseStats, DerivedStats


@dataclass
class Player:
    id: UUID
    user_id: UUID
    name: str
    race: RaceType
    archetype: ArchetypeType
    origin: OriginType
    base_stats: BaseStats
    derived_stats: DerivedStats
    current_hp: int
    current_mana: int
    save_version: int
    gold: int = 0
    narrative_flags: dict[str, Any] = field(default_factory=dict)
    active_demon_ids: list[str] = field(default_factory=list)

    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def spend_mana(self, amount: int) -> bool:
        if self.current_mana < amount:
            return False
        self.current_mana -= amount
        return True

    def restore_mana(self, amount: int) -> None:
        self.current_mana = min(self.derived_stats.mana, self.current_mana + amount)

    def set_flag(self, key: str, value: Any) -> None:
        self.narrative_flags[key] = value

    def get_flag(self, key: str, default: Any = None) -> Any:
        return self.narrative_flags.get(key, default)

    # Nível NÃO é propriedade do Player.
    # É calculado por DemonLevelService somando os níveis dos demônios em active_demon_ids.
    # Isso mantém a regra de nível da trilogia sem acoplar Player à entidade Demon.
