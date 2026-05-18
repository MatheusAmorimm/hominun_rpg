from enum import Enum


class ProgressionDomainId(str, Enum):
    DEMONIC_BOND = "demonic_bond"
    PERSONAL_COMBAT = "personal_combat"
    ETHER_KNOWLEDGE = "ether_knowledge"


class NodeTier(int, Enum):
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class ManaSource(str, Enum):
    PLAYER = "player"
    DEMON = "demon"
    BOTH = "both"
