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
from pydantic import field_validator

# if TYPE_CHECKING:
from .student import User
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
    created_by: str = Field(
        sa_column=Column(String,
                         ForeignKey("users.student_id"),
                         nullable=False),
        max_length=9,
        min_length=7
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

    creator: "User" = Relationship(back_populates="elections")
    candidates: list["Candidate"] = Relationship(back_populates="election")
    votes: list["Vote"] = Relationship(back_populates="election")

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v: datetime, info) -> datetime:
        values = info.data
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

    @field_validator('max_choices_per_voter')
    @classmethod
    def validate_max_choices(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError(
                'max_choices_per_voter must be a positive integer'
            )
        return v


class ElectionUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ElectionStatus] = None
    allow_multiple_choices: Optional[bool] = False
    max_choices_per_voter: Optional[int] = None
    is_published: Optional[bool] = None

    @field_validator('end_time')
    @classmethod
    def validate_end_time(
        cls, v: Optional[datetime], info
    ) -> Optional[datetime]:
        if not v:
            return v
        values = info.data
        if ('start_time' in values and
                values['start_time'] and v <= values['start_time']):
            raise ValueError('end_time must be after start_time')
        return v

    @field_validator('max_choices_per_voter')
    @classmethod
    def validate_max_choices(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError(
                'max_choices_per_voter must be a positive integer'
            )
        return v

    @field_validator('status')
    @classmethod
    def validate_status_transition(
        cls, v: Optional[ElectionStatus], info
    ) -> Optional[ElectionStatus]:
        if not v:
            return v
        values = info.data
        if (v == ElectionStatus.scheduled and
                values.get('end_time') and
                values['end_time'] < datetime.now(timezone.utc)):
            raise ValueError(
                'Cannot set status to scheduled for past elections'
            )
        return v
