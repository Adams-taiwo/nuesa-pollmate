from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String, Enum as SQLEnum, Boolean
from pydantic import ConfigDict
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
    student_id: str = Field(
        sa_column=Column(String,
                         primary_key=True,
                         unique=True,
                         index=True,
                         nullable=False)
    )

    matric_number: str = Field(
        default=None,
        sa_column=Column(String,
                         unique=True,
                         index=True,
                         nullable=False),
        # regex=r'^\d{4}/1/90\d{3}[A-Z]{2}$',
        description="Student matriculation number in format YYYY/N/NNNNNAA"
    )
    role: UserRole = Field(
        default=UserRole.student,
        sa_column=Column(SQLEnum(UserRole, name="user_role"), nullable=False)
    )
    is_active: bool = Field(
        default=True,
        exclude=True,
        sa_column=Column(Boolean, nullable=False)
    )


class User(UserBase, table=True):
    __tablename__: str = "users"

    candidacy: Optional["Candidate"] = Relationship(
        back_populates="user",
        # sa_relationship_kwargs={"uselist": False,
        #                         "foreign_keys": "Candidate.student_id"}
    )
    elections: list["Election"] = Relationship(back_populates="creator")
    vote: Optional["Vote"] = Relationship(back_populates="student")
    # votes: list["Vote"] = Relationship(back_populates="voter",)
                                    #    sa_relationship_kwargs={
                                    #     "foreign_keys": "Vote.student_id"})


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    student_id: str = Field(
        default=None,
        nullable=False,
    )
    matric_number: str = Field(
        default=None,
        nullable=False,
        # regex=r'^\d{4}/1/90\d{3}[A-Z]{2}$',
    )
