from abc import ABC, abstractmethod
from typing import Any

from server.domain.narrative.conditions.condition import Condition


class Trigger(ABC):
    def __init__(self, condition: Condition) -> None:
        self.condition = condition

    @abstractmethod
    def fire(self, flags: dict[str, Any]) -> list[str]:
        """Returns the consequence IDs to apply."""
        ...
