from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.infrastructure.database.base import get_db
from server.infrastructure.repositories.json.faction_repository import JsonFactionRepository
from server.infrastructure.repositories.json.npc_repository import JsonNpcRepository
from server.infrastructure.repositories.json.progression_repository import JsonProgressionRepository
from server.infrastructure.repositories.json.region_repository import JsonRegionRepository
from server.infrastructure.repositories.postgres.character_repository import PostgresCharacterRepository
from server.infrastructure.repositories.postgres.session_repository import PostgresSessionRepository
from server.use_cases.characters.create_character import CreateCharacterUseCase
from server.use_cases.characters.get_character import GetCharacterUseCase
from server.use_cases.factions.get_factions import GetFactionsUseCase
from server.use_cases.factions.get_reputations import GetReputationsUseCase
from server.use_cases.factions.update_reputation import UpdateReputationUseCase
from server.use_cases.npcs.get_npc import GetNpcUseCase
from server.use_cases.npcs.get_npcs import GetNpcsUseCase
from server.use_cases.progression.get_domains import GetProgressionDomainsUseCase
from server.use_cases.progression.unlock_node import UnlockNodeUseCase
from server.use_cases.regions.get_region import GetRegionUseCase
from server.use_cases.regions.get_regions import GetRegionsUseCase
from server.use_cases.regions.move_player import MovePlayerUseCase
from server.use_cases.sessions.create_session import CreateSessionUseCase
from server.use_cases.sessions.get_session import GetSessionUseCase


# JSON-backed repositories (static game content — load once, never changes at runtime)
@lru_cache(maxsize=1)
def _region_repo() -> JsonRegionRepository:
    return JsonRegionRepository()


@lru_cache(maxsize=1)
def _npc_repo() -> JsonNpcRepository:
    return JsonNpcRepository()


@lru_cache(maxsize=1)
def _faction_repo() -> JsonFactionRepository:
    return JsonFactionRepository()


@lru_cache(maxsize=1)
def _progression_repo() -> JsonProgressionRepository:
    return JsonProgressionRepository()


# PostgreSQL repositories — scoped per request via AsyncSession
def _character_repo(db: AsyncSession = Depends(get_db)) -> PostgresCharacterRepository:
    return PostgresCharacterRepository(db)


def _session_repo(db: AsyncSession = Depends(get_db)) -> PostgresSessionRepository:
    return PostgresSessionRepository(db)


# Use case factories

def get_create_character_uc(repo: PostgresCharacterRepository = Depends(_character_repo)) -> CreateCharacterUseCase:
    return CreateCharacterUseCase(repo)

def get_get_character_uc(repo: PostgresCharacterRepository = Depends(_character_repo)) -> GetCharacterUseCase:
    return GetCharacterUseCase(repo)

def get_get_regions_uc() -> GetRegionsUseCase:
    return GetRegionsUseCase(_region_repo())

def get_get_region_uc() -> GetRegionUseCase:
    return GetRegionUseCase(_region_repo())

def get_move_player_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> MovePlayerUseCase:
    return MovePlayerUseCase(_region_repo(), repo)

def get_get_npcs_uc() -> GetNpcsUseCase:
    return GetNpcsUseCase(_npc_repo())

def get_get_npc_uc() -> GetNpcUseCase:
    return GetNpcUseCase(_npc_repo())

def get_get_factions_uc() -> GetFactionsUseCase:
    return GetFactionsUseCase(_faction_repo())

def get_get_reputations_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> GetReputationsUseCase:
    return GetReputationsUseCase(_faction_repo(), repo)

def get_update_reputation_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> UpdateReputationUseCase:
    return UpdateReputationUseCase(_faction_repo(), repo)

def get_get_domains_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> GetProgressionDomainsUseCase:
    return GetProgressionDomainsUseCase(_progression_repo(), repo)

def get_unlock_node_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> UnlockNodeUseCase:
    return UnlockNodeUseCase(_progression_repo(), repo)

def get_create_session_uc(
    session_repo: PostgresSessionRepository = Depends(_session_repo),
    character_repo: PostgresCharacterRepository = Depends(_character_repo),
) -> CreateSessionUseCase:
    return CreateSessionUseCase(session_repo, character_repo)

def get_get_session_uc(repo: PostgresSessionRepository = Depends(_session_repo)) -> GetSessionUseCase:
    return GetSessionUseCase(repo)
