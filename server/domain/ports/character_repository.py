from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.entities.player import Player


class CharacterRepository(ABC):
    @abstractmethod
    async def save(self, player: Player) -> None: ...

    @abstractmethod
    async def get_by_id(self, character_id: UUID) -> Player | None: ...
