from enum import Enum


class ItemCategory(str, Enum):
    WEAPON = "weapon"
    CONSUMABLE = "consumable"
    MISC = "misc"


class WeaponType(str, Enum):
    SIMPLE_MELEE = "simple_melee"
    SIMPLE_RANGED = "simple_ranged"
    MARTIAL_MELEE = "martial_melee"
    MARTIAL_RANGED = "martial_ranged"


class DamageType(str, Enum):
    SLASHING = "slashing"
    PIERCING = "piercing"
    BLUDGEONING = "bludgeoning"


class WeaponProperty(str, Enum):
    FINESSE = "finesse"
    LIGHT = "light"
    HEAVY = "heavy"
    TWO_HANDED = "two_handed"
    REACH = "reach"
    VERSATILE = "versatile"
    THROWN = "thrown"
    AMMUNITION = "ammunition"
    LOADING = "loading"
    SPECIAL = "special"


class StatBonus(str, Enum):
    STR = "str"
    DEX = "dex"
    STR_OR_DEX = "str_or_dex"
