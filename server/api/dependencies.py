from functools import lru_cache

from server.infrastructure.repositories.json.character_repository import InMemoryCharacterRepository
from server.infrastructure.repositories.json.faction_repository import JsonFactionRepository
from server.infrastructure.repositories.json.npc_repository import JsonNpcRepository
from server.infrastructure.repositories.json.progression_repository import JsonProgressionRepository
from server.infrastructure.repositories.json.region_repository import JsonRegionRepository
from server.infrastructure.repositories.json.session_repository import InMemorySessionRepository
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

# Singleton repositories (in-memory state persists for the lifetime of the process)
_character_repo = InMemoryCharacterRepository()
_session_repo = InMemorySessionRepository()

# JSON-backed repositories (load once at startup)
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


# Use case factories — FastAPI calls these as Depends()

def get_create_character_uc() -> CreateCharacterUseCase:
    return CreateCharacterUseCase(_character_repo)

def get_get_character_uc() -> GetCharacterUseCase:
    return GetCharacterUseCase(_character_repo)

def get_get_regions_uc() -> GetRegionsUseCase:
    return GetRegionsUseCase(_region_repo())

def get_get_region_uc() -> GetRegionUseCase:
    return GetRegionUseCase(_region_repo())

def get_move_player_uc() -> MovePlayerUseCase:
    return MovePlayerUseCase(_region_repo(), _session_repo)

def get_get_npcs_uc() -> GetNpcsUseCase:
    return GetNpcsUseCase(_npc_repo())

def get_get_npc_uc() -> GetNpcUseCase:
    return GetNpcUseCase(_npc_repo())

def get_get_factions_uc() -> GetFactionsUseCase:
    return GetFactionsUseCase(_faction_repo())

def get_get_reputations_uc() -> GetReputationsUseCase:
    return GetReputationsUseCase(_faction_repo(), _session_repo)

def get_update_reputation_uc() -> UpdateReputationUseCase:
    return UpdateReputationUseCase(_faction_repo(), _session_repo)

def get_get_domains_uc() -> GetProgressionDomainsUseCase:
    return GetProgressionDomainsUseCase(_progression_repo(), _session_repo)

def get_unlock_node_uc() -> UnlockNodeUseCase:
    return UnlockNodeUseCase(_progression_repo(), _session_repo)

def get_create_session_uc() -> CreateSessionUseCase:
    return CreateSessionUseCase(_session_repo)

def get_get_session_uc() -> GetSessionUseCase:
    return GetSessionUseCase(_session_repo)
