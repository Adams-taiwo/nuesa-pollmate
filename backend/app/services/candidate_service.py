from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import (
    Depends, HTTPException, status, UploadFile)
import uuid
from sqlmodel import select
import os
import aiofiles

from ..schemas.candidate import (CandidateCreateSchema,
                                 CandidateUpdateSchema,
                                 CandidatePhotoUpload)
from ..models.candidate import Candidate
from ..models.election import Election
from ..models.student import User
from ..db.session import get_async_session


UPLOAD_DIR = "uploads/candidate_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_upload_file( file: UploadFile, filename: str) -> str:
    """Save an uploaded file and return its URL."""
    file_location = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return f"/uploads/candidate_photos/{filename}"


async def get_candidate_by_id(   
        candidate_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(Candidate).where(
        Candidate.candidate_id == candidate_id).options(
            joinedload(Candidate.election) # type: ignore
        )
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
    statement = select(User).where(
        User.student_id == candidate_data.student_id
    ).options(joinedload(Candidate.election)) # type: ignore
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Student with student_id {candidate_data.student_id}
            not found"""
        )

    statement = select(Candidate).where(
        Candidate.student_id == candidate_data.student_id
    ).options(joinedload(Candidate.election)) # type: ignore
    result = await session.execute(statement)
    existing_candidate = result.scalar_one_or_none()
    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Student with student_id {candidate_data.student_id}
            is already a candidate"""
        )

    statement = select(Election).where(
        Election.id == candidate_data.election_id
    )
    result = await session.execute(statement)
    election = result.scalar_one_or_none()
    if election is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Election with id {candidate_data.election_id}
            not found"""
        )

    candidate = Candidate(**candidate_data.model_dump())
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

    if candidate.photo_url:
        photo_path = os.path.join(
            UPLOAD_DIR,
            os.path.basename(candidate.photo_url)
        )
        if os.path.exists(photo_path):
            os.remove(photo_path)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )

    await session.delete(candidate)
    await session.commit()

    return {"message": f"Candidate with id {candidate_id} deleted"}
