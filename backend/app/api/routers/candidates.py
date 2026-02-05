from typing import List, Optional
from fastapi import (
    APIRouter, Depends, HTTPException, status
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from ...db.session import get_async_session
from ...models.candidate import Candidate
from ...schemas.candidate import CandidateRead


router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=List[CandidateRead])
async def list_candidates(
    election_id: Optional[UUID] = None,
    session: AsyncSession = Depends(get_async_session)
):
    statement = select(Candidate)

    if election_id is not None:
        statement = statement.where(
            Candidate.__table__.c.election_id == election_id)

    result = await session.execute(statement)
    return result.scalars().all()


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    statement = select(Candidate).where(
        Candidate.__table__.c.candidate_id == candidate_id
    )
    result = await session.execute(statement)
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return candidate
