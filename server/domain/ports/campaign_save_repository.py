from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.entities.campaign_save import CampaignSave


class CampaignSaveRepository(ABC):
    @abstractmethod
    async def save(self, campaign_save: CampaignSave) -> None: ...

    @abstractmethod
    async def get_by_id(self, save_id: UUID) -> CampaignSave | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[CampaignSave]: ...

    @abstractmethod
    async def list_by_session(self, session_id: str) -> list[CampaignSave]: ...

    @abstractmethod
    async def delete(self, save_id: UUID) -> None: ...
