from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

from ..models.election import StudentBodies, ElectionStatus
from ..models.candidate import Candidate


class CreateElection(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    student_body: Optional[StudentBodies]
    position: str
    created_by: str

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v: datetime, info) -> datetime:
        values = info.data
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class ElectionRead(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[str]
    student_body: Optional[StudentBodies]
    position: Optional[str]
    created_by: Optional[str]
    candidates: List[Candidate] = []

class UpdateElection(ElectionRead):
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(
        cls, v: Optional[datetime], info
    ) -> Optional[datetime]:
        if not v:
            return v
        values = info.data
        if ('start_time' in values and
                values['start_time'] and v <= values['start_time']):
            raise ValueError('end_time must be after start_time')
        return v

    @field_validator('status')
    @classmethod
    def validate_status_transition(
        cls, v: Optional[ElectionStatus], info
    ) -> Optional[ElectionStatus]:
        if not v:
            return v
        values = info.data
        if (v == ElectionStatus.scheduled and
                values.get('end_time') and
                values['end_time'] < datetime.now()):
            raise ValueError(
                'Cannot set status to scheduled for past elections'
            )
        return v
