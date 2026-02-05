from typing import TYPE_CHECKING, Dict
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, func, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
import uuid
from datetime import datetime, timezone
from pydantic import field_validator

if TYPE_CHECKING:
    from .candidate import Candidate
    from .election import Election


class VoteBase(SQLModel):
    student_id: str = Field(
        default="",
        sa_column=Column(String,
                         nullable=False)
    )
    election_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True),
                         ForeignKey("elections.id"),
                         nullable=False)
    )
    candidate_id: uuid.UUID = Field(
        default=None,
        sa_column=Column(PG_UUID(as_uuid=True),
                         ForeignKey("candidates.candidate_id"),
                         nullable=True)
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
    __tablename__ = "votes"

    id: str = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            index=True
        )
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False),
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(),
                         onupdate=func.now(), nullable=False),
    )

    candidate: "Candidate" = Relationship(back_populates="votes")
    election: "Election" = Relationship(back_populates="votes")
