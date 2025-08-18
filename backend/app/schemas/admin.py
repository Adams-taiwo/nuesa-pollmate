from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from ..models.election import ElectionStatus


class ElectionCreate(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    created_by: str
    status: ElectionStatus = ElectionStatus.scheduled
    is_published: bool = False
    allow_multiple_choices: bool = False
    max_choices_per_voter: Optional[int] = 1


class ElectionCreateResponse(BaseModel):
    message: str
    election_id: str


class ElectionUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[ElectionStatus]
    is_published: Optional[bool] = None


class AuditLogRead(BaseModel):
    id: str
    actor_id: Optional[str]
    action: str
    target_type: str
    target_id: str
    metadata_: dict
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )
