from uuid import UUID

from server.domain.entities.player import Player
from server.domain.ports.character_repository import CharacterRepository


class InMemoryCharacterRepository(CharacterRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Player] = {}

    async def save(self, player: Player) -> None:
        self._store[player.id] = player

    async def get_by_id(self, character_id: UUID) -> Player | None:
        return self._store.get(character_id)
