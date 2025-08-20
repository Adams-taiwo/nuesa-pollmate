from pydantic import BaseModel, Field
from datetime import datetime


class AuditLogBaseSchema(BaseModel):
    actor_student_id: str = Field(min_length=8,
                                  max_length=8,)
    #                              pattern=r'M\d{7}$'
    action: str
    target_type: str
    target_id: str
    metadata: dict


class AuditLogCreateSchema(AuditLogBaseSchema):
    pass


class AuditLogRead(AuditLogBaseSchema):
    id: str
    created_at: datetime
