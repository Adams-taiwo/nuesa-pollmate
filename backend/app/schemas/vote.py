from pydantic import BaseModel, Field
from uuid import UUID


class VoteCreateSchema(BaseModel):
    student_id: str
    election_id: UUID
    candidate_id: UUID
    ballot_id: str
    metadata: dict
