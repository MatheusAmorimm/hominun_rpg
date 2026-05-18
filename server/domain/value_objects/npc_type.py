from enum import Enum


class NpcAlignment(str, Enum):
    ALLY = "ally"
    NEUTRAL = "neutral"
    ANTAGONIST = "antagonist"
    COMPLEX = "complex"
    UNKNOWN = "unknown"


class NpcRole(str, Enum):
    LORD = "lord"
    LADY = "lady"
    KING = "king"
    QUEEN = "queen"
    SUMMONER = "summoner"
    TEACHER = "teacher"
    WARRIOR = "warrior"
    STUDENT = "student"
    CIVILIAN = "civilian"
    SPY = "spy"
    UNKNOWN = "unknown"


class NpcStatus(str, Enum):
    ALIVE = "alive"
    DECEASED = "deceased"
    MISSING = "missing"
    UNKNOWN = "unknown"
