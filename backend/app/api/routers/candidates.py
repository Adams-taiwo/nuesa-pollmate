from typing import List, Optional
from fastapi import (
    APIRouter, Depends, HTTPException, status,
    UploadFile, File, Form
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
import aiofiles
import os
from datetime import datetime

from ...db.session import get_async_session
from ...core.dependencies import get_admin_user
from ...models.candidate import Candidate
from ...models.election import Election
from ...schemas.candidate import (
    CandidateCreateSchema,
    CandidateRead,
    CandidateUpdateSchema,
)
from ...models.audit_log import AuditLog
from ...models.student import User

router = APIRouter(prefix="/candidates", tags=["candidates"])

# Configure upload directory
UPLOAD_DIR = "uploads/candidate_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_upload_file(file: UploadFile, filename: str) -> str:
    """Save an uploaded file and return its URL."""
    file_location = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return f"/uploads/candidate_photos/{filename}"


@router.post("", response_model=CandidateRead)
async def create_candidate(
    candidate: CandidateCreateSchema,
    photo: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin_user)
):
    """Create a new candidate."""
    # Verify user exists
    user_query = select(User).where(User.student_id == candidate.user_id)
    user_result = await session.execute(user_query)
    if not user_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify election exists
    election_query = select(Election).where(
        Election.id == candidate.election_id
    )
    election_result = await session.execute(election_query)
    if not election_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Election not found"
        )

    # Check if user is already a candidate
    existing_query = select(Candidate).where(
        Candidate.user_id == candidate.user_id
    )
    existing_result = await session.execute(existing_query)
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a candidate"
        )

    # Handle photo upload if provided
    photo_url = None
    if photo:
        filename = f"{candidate.user_id}_{datetime.now().timestamp()}_"\
                  f"{photo.filename}"
        photo_url = await save_upload_file(photo, filename)

    # Create candidate
    db_candidate = Candidate(
        **candidate.model_dump(),
        photo_url=photo_url
    )
    session.add(db_candidate)

    # Add audit log
    audit = AuditLog(
        actor_id=admin.id,
        action="candidate_created",
        target_type="candidate",
        target_id=str(db_candidate.id),
        metadata_={
            "election_id": str(candidate.election_id),
            "position": candidate.position
        }
    )
    session.add(audit)

    await session.commit()
    await session.refresh(db_candidate)
    return db_candidate


@router.get("", response_model=List[CandidateRead])
async def list_candidates(
    election_id: Optional[UUID] = None,
    position: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """List all candidates, optionally filtered by election or position."""
    query = select(Candidate)

    if election_id:
        query = query.where(Candidate.election_id == election_id)
    if position:
        query = query.where(Candidate.position == position)

    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific candidate by ID."""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return candidate


@router.patch("/{candidate_id}")
async def update_candidate(
    candidate_id: UUID,
    updates: CandidateUpdateSchema,
    photo: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin_user)
):
    """Update a candidate's information."""
    # Get existing candidate
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    if photo:
        if candidate.photo_url:
            # Remove old photo
            old_photo = os.path.join(
                UPLOAD_DIR,
                os.path.basename(candidate.photo_url)
            )
            if os.path.exists(old_photo):
                os.remove(old_photo)
        
        filename = f"{candidate.user_id}_{datetime.now().timestamp()}_"\
                  f"{photo.filename}"
        photo_url = await save_upload_file(photo, filename)
        updates.photo_url = photo_url

    # Update candidate
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(candidate, field, value)

    session.add(candidate)
    
    # Add audit log
    audit = AuditLog(
        actor_id=admin.id,
        action="candidate_updated",
        target_type="candidate",
        target_id=str(candidate.id),
        metadata_=updates.model_dump(exclude_unset=True)
    )
    session.add(audit)
    
    await session.commit()
    return {"message": "Candidate updated successfully"}


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin_user)
):
    """Delete a candidate."""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    # Remove photo if exists
    if candidate.photo_url:
        photo_path = os.path.join(
            UPLOAD_DIR,
            os.path.basename(candidate.photo_url)
        )
        if os.path.exists(photo_path):
            os.remove(photo_path)

    await session.delete(candidate)

    # Add audit log
    audit = AuditLog(
        actor_id=admin.id,
        action="candidate_deleted",
        target_type="candidate",
        target_id=str(candidate_id)
    )
    session.add(audit)

    await session.commit()
