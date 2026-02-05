# from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone

# if TYPE_CHECKING:
#     from .user import User


class AuditLogBase(SQLModel):
    actor_id: str = Field(
        default="",
        sa_column=Column(
            String,
            ForeignKey("users.student_id"),
            nullable=True
        )
    )
    action: str = Field(max_length=500, sa_column=Column(String, nullable=False))
    target_type: str = Field(sa_column=Column(String, nullable=False))
    target_id: str = Field(
        sa_column=Column(String,
                         nullable=False)
    )
    metadata_: dict = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSONB, nullable=False),
        alias="metadata"
    )


class AuditLog(AuditLogBase, table=True):
    __tablename__ = "audit_logs"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: uuid.UUID
    created_at: datetime
