from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.entities.player import Player
from server.domain.ports.character_repository import CharacterRepository
from server.domain.value_objects.race_type import ArchetypeType, OriginType, RaceType
from server.domain.value_objects.stats import BaseStats, DerivedStats
from server.infrastructure.orm_models.character_model import CharacterModel


def _to_domain(row: CharacterModel) -> Player:
    bs = row.base_stats
    ds = row.derived_stats
    return Player(
        id=row.id,
        user_id=row.user_id,
        name=row.name,
        race=RaceType(row.race),
        archetype=ArchetypeType(row.archetype),
        origin=OriginType(row.origin),
        base_stats=BaseStats(
            str_=bs["str_"], dex=bs["dex"], con=bs["con"],
            int_=bs["int_"], wis=bs["wis"], cha=bs["cha"],
        ),
        derived_stats=DerivedStats(
            hp=ds["hp"], mana=ds["mana"],
            initiative=ds["initiative"], ether_resistance=ds["ether_resistance"],
        ),
        current_hp=row.current_hp,
        current_mana=row.current_mana,
        save_version=row.save_version,
        gold=row.gold,
        narrative_flags=row.narrative_flags,
        active_demon_ids=row.active_demon_ids,
    )


class PostgresCharacterRepository(CharacterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, player: Player) -> None:
        existing = await self._session.get(CharacterModel, player.id)
        data = dict(
            user_id=player.user_id,
            name=player.name,
            race=player.race.value,
            archetype=player.archetype.value,
            origin=player.origin.value,
            current_hp=player.current_hp,
            current_mana=player.current_mana,
            gold=player.gold,
            save_version=player.save_version,
            base_stats={
                "str_": player.base_stats.str_, "dex": player.base_stats.dex,
                "con": player.base_stats.con, "int_": player.base_stats.int_,
                "wis": player.base_stats.wis, "cha": player.base_stats.cha,
            },
            derived_stats={
                "hp": player.derived_stats.hp, "mana": player.derived_stats.mana,
                "initiative": player.derived_stats.initiative,
                "ether_resistance": player.derived_stats.ether_resistance,
            },
            narrative_flags=player.narrative_flags,
            active_demon_ids=player.active_demon_ids,
        )
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
        else:
            self._session.add(CharacterModel(id=player.id, **data))

    async def get_by_id(self, character_id: UUID) -> Player | None:
        row = await self._session.get(CharacterModel, character_id)
        return _to_domain(row) if row else None
