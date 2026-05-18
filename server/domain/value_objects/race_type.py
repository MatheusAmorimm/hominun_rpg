from enum import Enum


class RaceType(str, Enum):
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"
    ORC = "orc"


class ArchetypeType(str, Enum):
    PURE_SUMMONER = "pure_summoner"
    BATTLE_MAGE = "battle_mage"
    ETHER_EXPLORER = "ether_explorer"


class OriginType(str, Enum):
    NOBLE = "noble"
    COMMONER = "commoner"
    WAR_ORPHAN = "war_orphan"
