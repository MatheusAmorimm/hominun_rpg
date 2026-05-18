from uuid import UUID

from server.domain.entities.player import Player
from server.domain.ports.character_repository import CharacterRepository
from server.shared.exceptions import EntityNotFoundError


class GetCharacterUseCase:
    def __init__(self, repo: CharacterRepository) -> None:
        self._repo = repo

    async def execute(self, character_id: UUID) -> Player:
        player = await self._repo.get_by_id(character_id)
        if not player:
            raise EntityNotFoundError(f"Personagem '{character_id}' não encontrado.")
        return player
