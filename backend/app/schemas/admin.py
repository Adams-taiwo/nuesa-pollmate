from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ElectionCreate(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    created_by: str


class ElectionCreateResponse(BaseModel):
    message: str
    election_id: str


class ElectionUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]


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
