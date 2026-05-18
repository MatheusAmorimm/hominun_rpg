from abc import ABC, abstractmethod
from typing import Any


class Consequence(ABC):
    @abstractmethod
    def apply(self, flags: dict[str, Any]) -> dict[str, Any]:
        """Returns the updated flags after applying this consequence."""
        ...
