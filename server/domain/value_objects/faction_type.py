from enum import Enum


class FactionType(str, Enum):
    POLITICAL = "political"
    MILITARY = "military"
    TRIBAL = "tribal"
    CRIMINAL = "criminal"
    RELIGIOUS = "religious"


class FactionAlignment(str, Enum):
    ALLY = "ally"
    NEUTRAL = "neutral"
    ANTAGONIST = "antagonist"
    COMPLEX = "complex"


class ReputationStatus(str, Enum):
    HOSTILE = "hostile"
    UNFRIENDLY = "unfriendly"
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    HONORED = "honored"
