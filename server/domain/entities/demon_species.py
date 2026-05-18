from dataclasses import dataclass

from server.domain.value_objects.demon_type import (
    AbilityType,
    CaptureDifficulty,
    DemonTemperament,
    EffectType,
    Rarity,
)


@dataclass(frozen=True)
class DemonAbility:
    id: str
    name: str
    type: AbilityType
    effect_type: EffectType
    description: str


@dataclass(frozen=True)
class DemonBaseStats:
    hp: int
    mana: int
    strength: int
    agility: int
    armor: int


@dataclass(frozen=True)
class DemonSpecies:
    id: str
    name: str
    level: int
    description: str
    rarity: Rarity
    temperament_base: DemonTemperament
    temperament_variants: frozenset[DemonTemperament]
    base_stats: DemonBaseStats
    abilities: tuple[DemonAbility, ...]
    habitat: tuple[str, ...]
    capture_difficulty: CaptureDifficulty
    known_summoners: tuple[str, ...]
    lore: str

    def has_ability(self, effect_type: EffectType) -> bool:
        return any(a.effect_type == effect_type for a in self.abilities)

    def is_capturable_without_preparation(self) -> bool:
        return self.capture_difficulty in (
            CaptureDifficulty.TRIVIAL,
            CaptureDifficulty.EASY,
            CaptureDifficulty.MODERATE,
        )
