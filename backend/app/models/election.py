from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import (
    Column,
    DateTime,
    func,
    String,
    Text,
    Boolean,
    ForeignKey,
    Integer,
    Enum as SQLEnum
    )
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .candidate import Candidate
    from .vote import Vote


# Election status enum
class ElectionStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    closed = "closed"
    cancelled = "cancelled"


class ElectionBase(SQLModel):
    title: str = Field(sa_column=Column(String, nullable=False))
    description: Optional[str] = Field(
        default=None, sa_column=Column(Text),
        )
    start_time: datetime = Field(sa_column=Column(DateTime(timezone=True),
                                                  nullable=False))
    end_time: datetime = Field(sa_column=Column(DateTime(timezone=True),
                                                nullable=False))
    status: ElectionStatus = Field(
        default=ElectionStatus.scheduled,
        sa_column=Column(SQLEnum(ElectionStatus, name="election_status"),
                         nullable=False)
    )
    allow_multiple_choices: bool = Field(default=False,
                                         sa_column=Column(Boolean,
                                                          nullable=False))
    max_choices_per_voter: Optional[int] = Field(default=1,
                                                 sa_column=Column(Integer))
    is_published: bool = Field(default=False,
                               sa_column=Column(Boolean, nullable=False))
    created_by: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True),
                         ForeignKey("users.id"),
                         nullable=False)
    )


class Election(ElectionBase, table=True):
    __tablename__ = "elections"

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
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    # Relationships
    creator: "User" = Relationship(back_populates="elections")
    candidates: list["Candidate"] = Relationship(back_populates="election")
    votes: list["Vote"] = Relationship(back_populates="election")


class ElectionCreate(ElectionBase):
    pass


class ElectionRead(ElectionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ElectionUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ElectionStatus] = None
    allow_multiple_choices: Optional[bool] = False
    max_choices_per_voter: Optional[int] = None
    is_published: Optional[bool] = None
