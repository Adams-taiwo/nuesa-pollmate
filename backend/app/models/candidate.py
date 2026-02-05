from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import (
    Column, DateTime, func, String, ForeignKey,
    Text, Boolean, UniqueConstraint, text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.types import JSON
import uuid
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .student import User
    from .election import Election
    from .vote import Vote


class CandidateBase(SQLModel):
    student_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("users.student_id"),
            nullable=False
        ),
        min_length=6,
        max_length=8,
    )
    election_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("elections.id"),
            nullable=False
        )
    )
    is_contesting: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default='true')
    )
    position: str = Field(sa_column=Column(String, nullable=False))
    bio: Optional[str] = Field(default=None, sa_column=Column(Text))
    manifesto: Optional[str] = Field(default=None, sa_column=Column(Text))
    achievements: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSONB,
                         nullable=False,
                         server_default=text("'[]'::jsonb"))
    )
    photo_url: Optional[str] = Field(default=None, sa_column=Column(String))


class Candidate(CandidateBase, table=True):
    __tablename__ = "candidates"
    __table_args__ = (
        UniqueConstraint("student_id",
                         "election_id",
                         name="uq_candidate_user_election"),
    )
    candidate_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(),
                         nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(),
                         onupdate=func.now(), nullable=False)
    )

    user: "User" = Relationship(back_populates="candidacy")
    election: "Election" = Relationship(back_populates="candidates")
    votes: list["Vote"] = Relationship(back_populates="candidate")


class CandidateUpdate(SQLModel):
    position: Optional[str] = None
    is_contesting: Optional[bool] = None
    bio: Optional[str] = None
    manifesto: Optional[str] = None
    achievements: Optional[List[str]] = Field(default=None,
                                              sa_column=Column(JSON))
    photo_url: Optional[str] = None
