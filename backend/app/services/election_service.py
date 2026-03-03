from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
import uuid
from ..models.election import Election
from ..schemas.election import CreateElection, UpdateElection
from ..db.session import get_async_session


async def get_election_by_id(
        election_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
) -> Election:
    statement = select(Election).where(
        Election.id == election_id
        ).options(selectinload(Election.candidates), selectinload(Election.votes)) # type: ignore
    result = await session.execute(statement)
    election = result.scalar_one_or_none()

    if election is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Election having id of {election_id} not found"
        )

    return election


async def create_election(
        election_data: CreateElection,
        session: AsyncSession = Depends(get_async_session)
) -> Election:
    election = Election(**election_data.model_dump())
    session.add(election)
    await session.commit()
    await session.refresh(election)

    return election


async def update_election(
        election_id: uuid.UUID,
        election_data: UpdateElection,
        session: AsyncSession = Depends(get_async_session)
) -> Election:
    election = await get_election_by_id(election_id, session)

    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Election have id of {election_id} not found"
        )

    update_data = election_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(election, key, value)

    await session.commit()
    await session.refresh(election)

    return election


async def delete_election(
        election_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    election = await get_election_by_id(election_id, session)
    election_title = election.title if election else "Election not found"

    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Election with id {election_id} not found"
        )

    await session.delete(election)
    await session.commit()

    return {"message": "Election deleted successfully",
            "election_title": str(election_title)}


# The logic in this function is outdated and no longer valid
async def toggle_election_status(
        election_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(Election).where(Election.id == election_id)
    result = await session.execute(statement)
    election = result.scalar_one_or_none()

    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Election having id {election_id} not found"
        )

    await session.commit()
    await session.refresh(election)

    return election
