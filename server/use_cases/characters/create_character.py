import json
from pathlib import Path
from uuid import UUID, uuid4

from server.domain.entities.player import Player
from server.domain.ports.character_repository import CharacterRepository
from server.domain.value_objects.race_type import ArchetypeType, OriginType, RaceType
from server.domain.value_objects.stats import BaseStats, DerivedStats
from server.shared.exceptions import EntityNotFoundError, InvalidActionError

_DATA_ROOT = Path(__file__).parents[3] / "data"


def _load_json(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class CreateCharacterUseCase:
    def __init__(self, repo: CharacterRepository) -> None:
        self._repo = repo
        self._races = {r["id"]: r for r in _load_json(_DATA_ROOT / "races" / "races.json")}
        self._archetypes = {a["id"]: a for a in _load_json(_DATA_ROOT / "archetypes" / "archetypes.json")}
        self._origins = {o["id"]: o for o in _load_json(_DATA_ROOT / "origins" / "origins.json")}

    async def execute(
        self,
        user_id: UUID,
        name: str,
        race: str,
        archetype: str,
        origin: str,
        bonus_stats: dict[str, int],
    ) -> Player:
        race_data = self._races.get(race)
        if not race_data:
            raise EntityNotFoundError(f"Raça '{race}' não encontrada.")

        archetype_data = self._archetypes.get(archetype)
        if not archetype_data:
            raise EntityNotFoundError(f"Archetype '{archetype}' não encontrado.")

        origin_data = self._origins.get(origin)
        if not origin_data:
            raise EntityNotFoundError(f"Origem '{origin}' não encontrada.")

        total_bonus = sum(bonus_stats.values())
        flexible_points = race_data.get("flexible_points", 0)
        if total_bonus > flexible_points:
            raise InvalidActionError(
                f"A raça '{race}' permite {flexible_points} pontos flexíveis, foram distribuídos {total_bonus}."
            )

        race_mods = race_data.get("stat_modifiers", {})
        arch_mods = archetype_data.get("stat_bonuses", {})

        base = BaseStats(
            str_=10 + race_mods.get("str", 0) + arch_mods.get("str", 0) + bonus_stats.get("str_", 0),
            dex=10 + race_mods.get("dex", 0) + arch_mods.get("dex", 0) + bonus_stats.get("dex", 0),
            con=10 + race_mods.get("con", 0) + arch_mods.get("con", 0) + bonus_stats.get("con", 0),
            int_=10 + race_mods.get("int", 0) + arch_mods.get("int", 0) + bonus_stats.get("int_", 0),
            wis=10 + race_mods.get("wis", 0) + arch_mods.get("wis", 0) + bonus_stats.get("wis", 0),
            cha=10 + race_mods.get("cha", 0) + arch_mods.get("cha", 0) + bonus_stats.get("cha", 0),
        )

        race_derived = race_data.get("derived_bonuses", {})
        derived = DerivedStats.from_base(
            base,
            hp_bonus=race_derived.get("hp", 0),
            mana_bonus=race_derived.get("mana", 0),
        )

        initial_flags: dict = {}
        for flag in origin_data.get("narrative_effects", []):
            initial_flags[flag] = True

        player = Player(
            id=uuid4(),
            user_id=user_id,
            name=name,
            race=RaceType(race),
            archetype=ArchetypeType(archetype),
            origin=OriginType(origin),
            base_stats=base,
            derived_stats=derived,
            current_hp=derived.hp,
            current_mana=10 + BaseStats.modifier(base.int_) * 2,
            save_version=1,
            gold=0,
            narrative_flags=initial_flags,
        )

        await self._repo.save(player)
        return player
