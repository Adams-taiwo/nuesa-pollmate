from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String, Enum as SQLEnum, Boolean
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
    student_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String,
                         primary_key=True,
                         unique=True,
                         index=True,
                         nullable=False),
        regex=r'^M\d{7}$',
        description="Student ID in format MYYNNNNN"
    )
    matric_number: str = Field(
        default=None,
        sa_column=Column(String,
                         unique=True,
                         index=True,
                         nullable=False),
        regex=r'^\d{4}/1/90\d{3}[A-Z]{2}$',
        description="Student matriculation number in format YYYY/1/NNNNN"
    )
    role: UserRole = Field(
        default=UserRole.student,
        sa_column=Column(SQLEnum(UserRole, name="user_role"), nullable=False)
    )
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False)
    )


class User(UserBase, table=True):
    __tablename__: str = "users"

    candidacy: Optional["Candidate"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )
    votes: list["Vote"] = Relationship(back_populates="voter")
    elections: list["Election"] = Relationship(back_populates="creator")


class UserCreate(UserBase):
    pass

    # model_config = ConfigDict(
    #     json_schema_extra={
    #         "example": {
    #             "matric_number": "2020/1/12345",
    #             "student_id": "M2312345",
    #             "password": "strongpassword123"
    #         }
    #     }
    # )


class UserRead(SQLModel):
    student_id: str
    matric_number: str
    role: UserRole
    is_active: bool

    # model_config = ConfigDict(
    #     "json_schema_extra": {
    #         "example": {
    #             "id": "123e4567-e89b-12d3-a456-426614174000",
    #             "student_id": "M2312345",
    #             "matric_number": "2020/1/12345",
    #             "role": "student",
    #             "is_active": True,
    #         }
    #     }
    # )


class UserUpdate(SQLModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    student_id: str = Field(
        default=None,
        regex=r'^M\d{7}$',
    )
    matric_number: str = Field(
        default=None,
        regex=r'^\d{4}/1/90\d{3}[A-Z]{2}$',
    )

    # model_config = ConfigDict(
    #     "json_schema_extra": {
    #         "example": {
    #             "student_id": "M2312345",
    #             "matric_number": "2020/1/12345",
    #         }
    #     }
    # )
