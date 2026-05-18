from abc import ABC, abstractmethod
from typing import Any


class Condition(ABC):
    @abstractmethod
    def evaluate(self, flags: dict[str, Any]) -> bool: ...
