from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.game_state.session_state import SessionState
from server.domain.ports.session_repository import SessionRepository
from server.infrastructure.orm_models.session_model import SessionModel


def _to_domain(row: SessionModel) -> SessionState:
    return SessionState(
        session_id=str(row.session_id),
        player_id=str(row.character_id),
        current_region=row.current_region,
        current_scene=row.current_scene,
        save_version=row.save_version,
        faction_reputations=row.faction_reputations,
        unlocked_nodes=row.unlocked_nodes,
        completed_milestones=row.completed_milestones,
        narrative_flags=row.narrative_flags,
    )


class PostgresSessionRepository(SessionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, state: SessionState) -> None:
        from uuid import UUID
        pk = UUID(state.session_id)
        existing = await self._session.get(SessionModel, pk)
        data = dict(
            current_region=state.current_region,
            current_scene=state.current_scene,
            save_version=state.save_version,
            faction_reputations=state.faction_reputations,
            unlocked_nodes=state.unlocked_nodes,
            completed_milestones=state.completed_milestones,
            narrative_flags=state.narrative_flags,
        )
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
        else:
            self._session.add(SessionModel(
                session_id=pk,
                character_id=UUID(state.player_id),
                **data,
            ))

    async def get_by_id(self, session_id: str) -> SessionState | None:
        from uuid import UUID
        row = await self._session.get(SessionModel, UUID(session_id))
        return _to_domain(row) if row else None
