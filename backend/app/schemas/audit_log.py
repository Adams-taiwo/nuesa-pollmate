from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class AuditLogBaseSchema(BaseModel):
    actor_id: str = Field(min_length=8,
                          max_length=8,)
    #                              pattern=r'M\d{7}$'
    action: str
    target_type: str
    target_id: str
    metadata: dict


class AuditLogCreateSchema(AuditLogBaseSchema):
    pass


class AuditLogReadSchema(AuditLogBaseSchema):
    id: uuid.UUID
    created_at: datetime
