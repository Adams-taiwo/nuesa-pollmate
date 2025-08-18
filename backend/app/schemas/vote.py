from pydantic import BaseModel, Field
from uuid import UUID


class VoteSchema(BaseModel):
    id: UUID
    student_id: str
    election_id: UUID
    candidate_id: UUID
    ballot_id: str
    metadata: dict
