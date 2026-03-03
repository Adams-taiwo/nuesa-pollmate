from pydantic import BaseModel, Field, ConfigDict

from ..models.student import UserRole


class UserBase(BaseModel):
    student_id: str = Field(min_length=8, max_length=8)
    matric_number: str = Field(min_length=14,
                               max_length=14,)
    #                           pattern=r'd{4}/1/\d{4}[A-Z]{2}$'


class UserCreateSchema(UserBase):
    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "matric_number": "2020/1/12345YY",
                "student_id": "M2312345",
                "password": "strong_passwd123"
            }
        }
    )


class AdminCreateSchema(UserCreateSchema):
    role: UserRole = Field(default=UserRole.admin)


class UserRead(BaseModel):
    student_id: str
    matric_number: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,  # Add this line
        json_schema_extra= {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "student_id": "M2312345",
                "matric_number": "2020/1/12345",
                "role": "student",
                "is_active": True,
            }
        }
    )


class StudentLogin(UserBase):
    
    model_config = ConfigDict(
        json_schema_extra= {
            "example": {
                "student_id": "M2312345",
                "matric_number": "2020/1/12345",
            }
        }
    )

# {
#   "matric_number": "2023/1/12345ET",
#   "student_id": "M0987654"
# }
