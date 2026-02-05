from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from ..models.election import ElectionStatus
from uuid import UUID


class ElectionCreateSchema(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    created_by: str
    status: ElectionStatus
    is_published: bool = False
    allow_multiple_choices: bool = False
    max_choices_per_voter: Optional[int] = 1


class ElectionCreateResponse(BaseModel):
    # message: str
    id: UUID
    title: str
    description: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class ElectionUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[ElectionStatus]
    is_published: Optional[bool] = None


class AuditLogReadSchema(BaseModel):
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
