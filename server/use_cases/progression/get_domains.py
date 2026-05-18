from server.api.schemas.progression import NodeState
from server.domain.ports.progression_repository import ProgressionRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError


class GetProgressionDomainsUseCase:
    def __init__(self, progression_repo: ProgressionRepository, session_repo: SessionRepository) -> None:
        self._progression_repo = progression_repo
        self._session_repo = session_repo

    async def execute(self, session_id: str, archetype: str, total_demon_level: int) -> list[dict]:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")

        domains = await self._progression_repo.get_all_domains()
        unlocked = frozenset(session.unlocked_nodes)
        milestones = frozenset(session.completed_milestones)

        result = []
        for domain in domains:
            available = frozenset(
                n.id for n in domain.available_nodes(total_demon_level, milestones, unlocked, archetype)
            )
            nodes = []
            for node in domain.nodes:
                if node.id in unlocked:
                    state = NodeState.UNLOCKED
                elif node.id in available:
                    state = NodeState.AVAILABLE
                else:
                    state = NodeState.LOCKED
                nodes.append({**node.__dict__, "state": state})

            result.append({"id": domain.id.value, "name": domain.name, "primary_archetype": domain.primary_archetype, "nodes": nodes})

        return result
