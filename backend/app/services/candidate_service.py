from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
import uuid
from sqlmodel import select

from ..schemas.candidate import (CandidateCreateSchema,
                                 CandidateUpdateSchema,
                                 CandidatePhotoUpload)
from ..models.candidate import Candidate
from ..db.session import get_async_session


async def get_candidate_by_id(
        candidate_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(Candidate).where(Candidate.candidate_id == candidate_id)
    result = await session.execute(statement)
    candidate = result.scalar_one_or_none()

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate having id of {candidate_id} not found"
        )

    return candidate


async def create_candidate(
        candidate_data: CandidateCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    candidate = CandidateCreateSchema(**candidate_data.model_dump())
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)

    return candidate


async def update_candidate(
        candidate_id: uuid.UUID,
        candidate_data: CandidateUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    candidate = await get_candidate_by_id(candidate_id, session)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )

    for key, value in candidate_data.model_dump(exclude_unset=True).items():
        setattr(candidate, key, value)

    await session.commit()
    await session.refresh(candidate)

    return candidate


async def upload_candidate_photo(
        candidate_id: uuid.UUID,
        photo: CandidatePhotoUpload,
        session: AsyncSession = Depends(get_async_session)
):
    candidate = await get_candidate_by_id(candidate_id, session)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )

    candidate.photo = photo.photo
    await session.commit()
    await session.refresh(candidate)

    return candidate


async def delete_candidate(
        candidate_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    candidate = await get_candidate_by_id(candidate_id, session)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )

    await session.delete(candidate)
    await session.commit()

    return {"message": f"Candidate with id {candidate_id} deleted successfully"}
