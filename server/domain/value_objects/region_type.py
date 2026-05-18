from enum import Enum


class RegionType(str, Enum):
    URBAN = "urban"
    RURAL = "rural"
    WILDERNESS = "wilderness"
    ETHER = "ether"
    FRONTIER = "frontier"


class DangerLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

    def is_lethal_without_preparation(self) -> bool:
        return self in (DangerLevel.HIGH, DangerLevel.EXTREME)
