from server.domain.ports.progression_repository import ProgressionRepository
from server.domain.ports.session_repository import SessionRepository
from server.shared.exceptions import EntityNotFoundError, InvalidActionError


class UnlockNodeUseCase:
    def __init__(self, progression_repo: ProgressionRepository, session_repo: SessionRepository) -> None:
        self._progression_repo = progression_repo
        self._session_repo = session_repo

    async def execute(
        self,
        session_id: str,
        node_id: str,
        archetype: str,
        total_demon_level: int,
    ) -> dict:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            raise EntityNotFoundError(f"Sessão '{session_id}' não encontrada.")

        if node_id in session.unlocked_nodes:
            raise InvalidActionError(f"Nó '{node_id}' já está desbloqueado.")

        domain = await self._progression_repo.get_node_domain(node_id)
        if not domain:
            raise EntityNotFoundError(f"Nó '{node_id}' não encontrado em nenhum domínio.")

        node = domain.get_node(node_id)
        milestones = frozenset(session.completed_milestones)
        unlocked = frozenset(session.unlocked_nodes)

        if not node.is_unlockable(total_demon_level, milestones, archetype, domain.id):
            eff_level = node._effective_level_requirement(archetype, domain.id)
            if total_demon_level < eff_level:
                raise InvalidActionError(
                    f"Nível de demônios insuficiente (requer {eff_level}, atual {total_demon_level})."
                )
            raise InvalidActionError(
                f"Marco narrativo '{node.narrative_milestone}' ainda não foi completado."
            )

        session.unlocked_nodes.append(node_id)
        await self._session_repo.save(session)

        return {"node_id": node_id, "unlocked_nodes": session.unlocked_nodes}
