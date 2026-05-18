from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class CampaignSave:
    id: UUID
    session_id: str
    user_id: UUID
    slot_name: str
    act: int
    current_region: str
    created_at: datetime
    state_snapshot: dict[str, Any]
