from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, func, String, Enum as SQLEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .candidate import Candidate
    from .vote import Vote
    from .election import Election


# User role enum
class UserRole(str, Enum):
    student = "student"
    admin = "admin"


class UserBase(SQLModel):
    matric_number: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False),
        regex=r'^\d{4}/1/\d{5}$',
        description="Student matriculation number in format YYYY/1/NNNNN"
    )
    student_id: Optional[str] = Field(  # Corrected type hint
        default=None,
        sa_column=Column(String,
                         unique=True,
                         index=True,
                         nullable=False),
        regex=r'^[A-Z]\d{8}$',
        description="Student ID in format MYYNNNNN"
    )
    role: UserRole = Field(
        default=UserRole.student,
        sa_column=Column(SQLEnum(UserRole, name="user_role"), nullable=False)
    )
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False)
    )
    hashed_password: str = Field(
        sa_column=Column(String, nullable=False),
        exclude=True  # Don't include in JSON responses
    )
    salt: str = Field(
        sa_column=Column(String, nullable=False),
        exclude=True  # Don't include in JSON responses
    )


class User(UserBase, table=True):
    __tablename__: str = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),  # Corrected
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),  # Corrected
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    # Relationships
    candidacy: Optional["Candidate"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )
    votes: list["Vote"] = Relationship(back_populates="voter")
    # Elections created by this user (creator)
    elections: list["Election"] = Relationship(back_populates="creator")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    model_config = {
        "json_schema_extra": {
            "example": {
                "matric_number": "2020/1/12345",
                "student_id": "M20123456",
                "password": "strongpassword123"
            }
        }
    }


class UserRead(SQLModel):
    id: uuid.UUID
    matric_number: str
    student_id: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "matric_number": "2020/1/12345",
                "student_id": "M20123456",
                "role": "student",
                "is_active": True,
                "created_at": "2025-08-16T12:00:00Z",
                "updated_at": "2025-08-16T12:00:00Z"
            }
        }
    }




class UserUpdate(SQLModel):
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    matric_number: str
    student_id: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "matric_number": "2020/1/12345",
                "student_id": "M20123456",
                "password": "strongpassword123"
            }
        }
    }
