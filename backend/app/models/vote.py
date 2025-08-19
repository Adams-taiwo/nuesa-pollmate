from typing import TYPE_CHECKING, Optional, Dict
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from pydantic import field_validator

if TYPE_CHECKING:
    from .student import User
    from .candidate import Candidate
    from .election import Election


class VoteBase(SQLModel):
    student_id: str = Field(
        default=None,
        sa_column=Column(String,
                         ForeignKey("users.student_id"),
                         nullable=False)
    )
    election_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("elections.id"),
                         nullable=False)
    )
    candidate_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(UUID(as_uuid=True),
                         ForeignKey("candidates.candidate_id"),
                         nullable=True)
    )
    ballot_token: Optional[str] = Field(
        default=None,
        sa_column=Column(String, nullable=True)
    )
    metadata_: Dict = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSONB, nullable=False),
    )

    @field_validator("metadata_")
    @classmethod
    def validate_metadata(cls, v: Dict) -> Dict:
        if not isinstance(v, dict):
            raise ValueError("metadata must be a dictionary")
        return v


class Vote(VoteBase, table=True):
    __tablename__ = "votes"  # SQLModel manages this internally

    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          sa_column=Column(UUID(as_uuid=True), primary_key=True))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

    voter: "User" = Relationship(back_populates="votes")
    candidate: Optional["Candidate"] = Relationship(back_populates="votes")
    election: "Election" = Relationship(back_populates="votes")
