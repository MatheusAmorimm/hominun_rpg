from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from server.domain.value_objects.item_type import (
    DamageType,
    ItemCategory,
    StatBonus,
    WeaponProperty,
    WeaponType,
)


@dataclass(frozen=True)
class WeaponRange:
    normal: int
    long: int


@dataclass(frozen=True)
class ItemEffect:
    type: str
    value: Any
    duration_turns: int = -1
    stat_cost: str | None = None


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    description: str
    category: ItemCategory
    value_gold: int
    weight: float
    lore: str


@dataclass(frozen=True)
class Weapon(Item):
    weapon_type: WeaponType
    damage_dice: str
    damage_type: DamageType
    stat_bonus: StatBonus
    properties: frozenset[WeaponProperty]
    versatile_dice: str | None = None
    range: WeaponRange | None = None
    special: str | None = None

    def is_ranged(self) -> bool:
        return self.weapon_type in (WeaponType.SIMPLE_RANGED, WeaponType.MARTIAL_RANGED)

    def is_finesse(self) -> bool:
        return WeaponProperty.FINESSE in self.properties

    def is_versatile(self) -> bool:
        return WeaponProperty.VERSATILE in self.properties

    def has_reach(self) -> bool:
        return WeaponProperty.REACH in self.properties

    def applicable_stat(self, player_str_mod: int, player_dex_mod: int) -> int:
        if self.stat_bonus == StatBonus.STR:
            return player_str_mod
        if self.stat_bonus == StatBonus.DEX:
            return player_dex_mod
        return max(player_str_mod, player_dex_mod)


@dataclass(frozen=True)
class Consumable(Item):
    effect: ItemEffect
    quantity_per_slot: int = 1


@dataclass(frozen=True)
class MiscItem(Item):
    quest_item: bool = False
    narrative_flags: dict[str, Any] = field(default_factory=dict)
