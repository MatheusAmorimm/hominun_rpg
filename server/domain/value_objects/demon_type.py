from enum import Enum


class DemonTemperament(str, Enum):
    AGGRESSIVE = "aggressive"
    PROTECTIVE = "protective"
    CAUTIOUS = "cautious"
    TERRITORIAL = "territorial"
    CRUEL = "cruel"
    LOYAL = "loyal"
    UNPREDICTABLE = "unpredictable"
    NOBLE = "noble"
    SOLITARY = "solitary"
    SOCIAL = "social"


class AbilityType(str, Enum):
    ACTIVE = "active"
    PASSIVE = "passive"
    REACTION = "reaction"


class EffectType(str, Enum):
    DAMAGE_PHYSICAL = "damage_physical"
    DAMAGE_FIRE = "damage_fire"
    DAMAGE_ELECTRIC = "damage_electric"
    DAMAGE_ICE = "damage_ice"
    DAMAGE_VENOM = "damage_venom"
    PARALYSIS = "paralysis"
    FREEZE = "freeze"
    BLIND = "blind"
    SILK = "silk"
    HEAL = "heal"
    CAMOUFLAGE = "camouflage"
    SCOUT = "scout"
    SWARM = "swarm"


class Rarity(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"


class CaptureDifficulty(str, Enum):
    TRIVIAL = "trivial"
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"
    EXTREME = "extreme"
    LEGENDARY = "legendary"
