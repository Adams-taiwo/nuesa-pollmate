from pydantic import BaseModel
from uuid import UUID


class VoteCreateSchema(BaseModel):
    student_id: str
    election_id: UUID
    candidate_id: UUID
    metadata: dict
