from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from server.api.dependencies import get_create_character_uc, get_get_character_uc
from server.api.middleware.auth import get_current_user
from server.api.schemas.character import (
    BaseStatsResponse,
    CharacterResponse,
    CreateCharacterRequest,
    DerivedStatsResponse,
)
from server.domain.entities.player import Player
from server.domain.entities.user import User
from server.shared.exceptions import EntityNotFoundError, InvalidActionError
from server.use_cases.characters.create_character import CreateCharacterUseCase
from server.use_cases.characters.get_character import GetCharacterUseCase

router = APIRouter(prefix="/characters", tags=["characters"])


def _player_to_response(player: Player) -> CharacterResponse:
    return CharacterResponse(
        id=player.id,
        name=player.name,
        race=player.race.value,
        archetype=player.archetype.value,
        origin=player.origin.value,
        base_stats=BaseStatsResponse(
            str_=player.base_stats.str_,
            dex=player.base_stats.dex,
            con=player.base_stats.con,
            int_=player.base_stats.int_,
            wis=player.base_stats.wis,
            cha=player.base_stats.cha,
        ),
        derived_stats=DerivedStatsResponse(
            hp=player.derived_stats.hp,
            mana=player.derived_stats.mana,
            initiative=player.derived_stats.initiative,
            ether_resistance=player.derived_stats.ether_resistance,
        ),
        current_hp=player.current_hp,
        current_mana=player.current_mana,
        gold=player.gold,
        narrative_flags=player.narrative_flags,
        active_demon_ids=player.active_demon_ids,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CharacterResponse)
async def create_character(
    body: CreateCharacterRequest,
    current_user: User = Depends(get_current_user),
    uc: CreateCharacterUseCase = Depends(get_create_character_uc),
) -> CharacterResponse:
    try:
        player = await uc.execute(
            user_id=current_user.id,
            name=body.name,
            race=body.race,
            archetype=body.archetype,
            origin=body.origin,
            bonus_stats=body.bonus_stat_distribution.model_dump(),
        )
        return _player_to_response(player)
    except (EntityNotFoundError, InvalidActionError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: UUID,
    _: User = Depends(get_current_user),
    uc: GetCharacterUseCase = Depends(get_get_character_uc),
) -> CharacterResponse:
    try:
        player = await uc.execute(character_id)
        return _player_to_response(player)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
