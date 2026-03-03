from pydantic import BaseModel, ConfigDict, TypeAdapter
from typing import Optional, List
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
    position: Optional[str]


class ElectionCreateResponse(BaseModel):
    # message: str
    id: UUID
    title: str
    description: str
    position: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
    )


class ElectionUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[ElectionStatus]
    position: Optional[str]


class AuditLogReadSchema(BaseModel):
    id: UUID
    actor_id: Optional[str]
    action: str
    target_type: str
    target_id: str
    metadata_: dict
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


AuditLogAdapter = TypeAdapter(List[AuditLogReadSchema])
