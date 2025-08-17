from typing import Optional
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.vote import Vote


async def cast_vote_safe(
    session: AsyncSession,
    *,
    voter_id,
    election_id,
    candidate_id: Optional[str] = None,
    metadata: Optional[dict] = None,
    ballot_token: Optional[str] = None,
) -> bool:
    """Attempt to insert a vote using PostgreSQL ON CONFLICT DO NOTHING.

    Returns True when inserted, False on conflict (already voted).
    """
    metadata = metadata or {}
    stmt = pg_insert(Vote.__table__).values(
        voter_id=voter_id,
        election_id=election_id,
        candidate_id=candidate_id,
        ballot_token=ballot_token,
        metadata=metadata,
    ).on_conflict_do_nothing(index_elements=["election_id", "voter_id"])

    try:
        result = await session.execute(stmt)
        await session.commit()
        return (result.rowcount or 0) > 0
    except IntegrityError:
        await session.rollback()
        return False
