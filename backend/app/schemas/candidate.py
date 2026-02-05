from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from fastapi import UploadFile


class CandidatePhotoUpload(BaseModel):
    candidate_id: UUID
    photo: UploadFile = Field(..., description="Candidate's image")


class CandidateCreateSchema(BaseModel):
    student_id: str
    election_id: UUID
    position: str
    bio: Optional[str] = None
    manifesto: Optional[str] = None
    achievements: Optional[list[str]] = Field(default_factory=list)
    photo_url: Optional[str] = None
    is_contesting: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "student_id": "M2345678",
                "election_id": "123e4567-e89b-12d3-a456-426614174001",
                "position": "SUG President",
                "bio": "A dedicated student leader with 3 years of experience",
                "manifesto": """1. Improve student welfare\n
                2. Enhance academic resources""",
                "achievements": [
                    "Former Departmental President",
                    "Former Faculty President"
                ]
            }
        })


class CandidateUpdateSchema(BaseModel):
    position: Optional[str] = None
    bio: Optional[str] = None
    manifesto: Optional[str] = None
    achievements: Optional[list[str]] = None
    photo_url: Optional[str] = None
    is_contesting: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "position": "Public Relations Officer",
                "bio": "More detailed bio",
                "manifesto": "Updated manifesto",
                "achievements": ["Some New achievements"],
                "photo_url": """
                https://POLLMate/photos/candidate123.jpg
                """,
                "is_contesting": True
            }
        })


class CandidateRead(BaseModel):
    student_id: str
    election_id: UUID
    position: str
    bio: str
    manifesto: str
    achievements: list[str]
    photo_url: str
    is_contesting: bool
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "election_id": "123e4567-e89b-12d3-a456-426614174002",
                "position": "President",
                "bio": "A dedicated student leader",
                "manifesto": """1. Improve student welfare\n"
                2. Enhance academic resources""",
                "achievements": [
                    "Former class representative",
                    "Academic excellence award recipient"
                ],
                "photo_url": """
                https://POLLMate/photos/candidate123.jpg
                """,
                "created_at": "2025-08-16T12:00:00Z",
                "updated_at": "2025-08-16T12:00:00Z"
            }
        }
