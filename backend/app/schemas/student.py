from pydantic import BaseModel, Field

from ..models.student import UserRole


class UserBase(BaseModel):
    student_id: str = Field(min_length=8, max_length=8)
    matric_number: str = Field(min_length=14,
                               max_length=14,)
    #                           pattern=r'd{4}/1/\d{4}[A-Z]{2}$'


class UserCreateSchema(UserBase):
    is_active: bool


class AdminCreateSchema(UserCreateSchema):
    role: UserRole  # = Field(default=UserRole.admin)


class UserRead(BaseModel):
    student_id: str
    matric_number: str
    role: UserRole
    is_active: bool


class StudentLogin(UserBase):
    student_id: str = Field(min_length=8, max_length=8,)  # pattern=r'^M\d{7}$'
    matric_number: str = Field(min_length=14,
                               max_length=14,)
    #                           pattern=r'\d{4}/1/\d{4}[A-Z]{2}$'
