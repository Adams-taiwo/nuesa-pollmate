from pydantic import BaseModel, Field


class StudentLogin(BaseModel):
    student_id: str = Field(min_length=8, max_length=8, pattern=r'^M\d{7}$')
    matric_number: str
