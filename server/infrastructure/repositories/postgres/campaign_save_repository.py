from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.entities.campaign_save import CampaignSave
from server.domain.ports.campaign_save_repository import CampaignSaveRepository
from server.infrastructure.orm_models.campaign_save_model import CampaignSaveModel


def _to_domain(row: CampaignSaveModel) -> CampaignSave:
    return CampaignSave(
        id=row.id,
        session_id=str(row.session_id),
        user_id=row.user_id,
        slot_name=row.slot_name,
        act=row.act,
        current_region=row.current_region,
        created_at=row.created_at,
        state_snapshot=row.state_snapshot,
    )


class PostgresCampaignSaveRepository(CampaignSaveRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, campaign_save: CampaignSave) -> None:
        existing = await self._session.get(CampaignSaveModel, campaign_save.id)
        if existing:
            existing.slot_name = campaign_save.slot_name
            existing.act = campaign_save.act
            existing.current_region = campaign_save.current_region
            existing.state_snapshot = campaign_save.state_snapshot
        else:
            self._session.add(CampaignSaveModel(
                id=campaign_save.id,
                session_id=UUID(campaign_save.session_id),
                user_id=campaign_save.user_id,
                slot_name=campaign_save.slot_name,
                act=campaign_save.act,
                current_region=campaign_save.current_region,
                state_snapshot=campaign_save.state_snapshot,
            ))

    async def get_by_id(self, save_id: UUID) -> CampaignSave | None:
        row = await self._session.get(CampaignSaveModel, save_id)
        return _to_domain(row) if row else None

    async def list_by_user(self, user_id: UUID) -> list[CampaignSave]:
        result = await self._session.execute(
            select(CampaignSaveModel)
            .where(CampaignSaveModel.user_id == user_id)
            .order_by(CampaignSaveModel.created_at.desc())
        )
        return [_to_domain(row) for row in result.scalars()]

    async def list_by_session(self, session_id: str) -> list[CampaignSave]:
        result = await self._session.execute(
            select(CampaignSaveModel)
            .where(CampaignSaveModel.session_id == UUID(session_id))
            .order_by(CampaignSaveModel.created_at.desc())
        )
        return [_to_domain(row) for row in result.scalars()]

    async def delete(self, save_id: UUID) -> None:
        row = await self._session.get(CampaignSaveModel, save_id)
        if row:
            await self._session.delete(row)
