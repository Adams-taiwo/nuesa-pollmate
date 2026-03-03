from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from ..db.session import get_async_session
from ..models.vote import Vote
from ..models.student import User
from ..schemas.vote import VoteCreateSchema
from .candidate_service import get_candidate_by_id
from .election_service import get_election_by_id
from .student_service import get_user


async def create_voter(
        voter_data: VoteCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    voter = Vote(**voter_data.model_dump())

    _ = await get_user(voter_data.student_id, session)

    voter.candidate = await get_candidate_by_id(voter_data.candidate_id,
                                                session)
    voter.election = await get_election_by_id(voter_data.election_id, session)
    session.add(voter)
    await session.commit()
    await session.refresh(voter)

    return voter


async def delete_voter(
        voter_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(Vote).where(Vote.student_id == voter_id)
    result = await session.execute(statement)
    voter_to_delete = result.scalar_one_or_none()

    if voter_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Voter having student id of {voter_id} not found"
        )

    await session.delete(voter_to_delete)
    await session.commit()
    return {"message": f"Voter having voter id of {voter_id} deleted"}
