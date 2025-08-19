from fastapi import APIRouter, Depends, HTTPException, status, File
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...schemas import (admin as admin_schemas,
                        candidate as candidate_schemas,
                        vote as vote_schemas)
from ...db.session import get_async_session
from ...models.election import Election
from ...models.audit_log import AuditLog
from ...models.candidate import Candidate
from ...models.student import User
from ...services import (admin_service,
                         election_service,
                         candidate_service,
                         voter_service)

from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/elections", response_model=admin_schemas.ElectionCreateResponse)
async def create_election(
    payload: admin_schemas.ElectionCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    election = await election_service.create_election(payload, session)

    # audit = AuditLog(
    #     actor_id=payload.created_by,
    #     action="election_created",
    #     target_type="election",
    #     target_id=str(election.id),
    # )
    # session.add(audit)
    # await session.commit()

    return election


@router.put("/elections/{election_id}",
            response_model=admin_schemas.ElectionCreateResponse)
async def update_election(
    election_id: UUID,
    payload: admin_schemas.ElectionUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    election = await election_service.update_election(
        election_id, payload, session)

    # audit log
    # audit = AuditLog(
    #     actor_id=admin if hasattr(admin, "id") else None,
    #     action="election_updated",
    #     target_type="election",
    #     target_id=str(election.id),
    # )
    # session.add(audit)
    # await session.commit()

    return election


@router.delete(
    "/elections/{election_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_election(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    _ = await election_service.delete_election(election_id, session)

    # audit
    # audit = AuditLog(
    #     actor_id=admin if hasattr(admin, "id") else None,
    #     action="election_deleted",
    #     target_type="election",
    #     target_id=str(election.id),
    # )
    # session.add(audit)
    # await session.commit()

    return


@router.get("/audit/logs",
            response_model=List[admin_schemas.AuditLogReadSchema])
async def get_audit_logs(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    created_col = AuditLog.__table__.c.created_at
    q = select(AuditLog).order_by(created_col.desc()).limit(limit)
    result = await session.execute(q)
    logs = result.scalars().all()
    return [
        admin_schemas.AuditLogReadSchema.model_validate(log) for log in logs
        ]


@router.get("/db/schema")
async def get_db_schema(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    from sqlalchemy import text

    result = await session.execute(
        text("""
             SELECT table_name FROM information_schema.tables
             WHERE table_schema='public';
             """)
    )
    tables = [r[0] for r in result.fetchall()]
    return {"tables": tables}


@router.post("/candidates")
async def add_candidate(
    payload: candidate_schemas.CandidateCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
  ):
    candidate = await candidate_service.create_candidate(
        payload, session
    )
    # audit = AuditLog(
    #     actor_id=admin if hasattr(admin, "id") else None,
    #     action="candidate_added", target_type="candidate",
    #     target_id=str(candidate.student_id)
    #     )
    # session.add(audit)
    # await session.commit()
    return candidate


@router.patch("/candidates/{candidate_id}")
async def update_candidate(
    candidate_id: UUID,
    payload: candidate_schemas.CandidateUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    updated_candidate = await candidate_service.update_candidate(
        candidate_id, payload, session
    )

    # audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
    #                  action="candidate_updated",
    #                  target_type="candidate",
    #                  target_id=str(candidate.id))
    # session.add(audit)
    # await session.commit()
    return updated_candidate


@router.delete(
        "/candidates/{candidate_id}",
        status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    _ = await candidate_service.delete_candidate(
        candidate_id, session
    )
    # audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
    #                  action="candidate_deleted",
    #                  target_type="candidate",
    #                  target_id=str(candidate.id))
    # session.add(audit)
    # await session.commit()
    return


@router.post("/voters")
async def add_voter(payload: vote_schemas.VoteCreateSchema,
                    session: AsyncSession = Depends(get_async_session),
                    admin=Depends(admin_service.get_admin_user)):
    voter = await voter_service.create_vote(payload, session)
    # audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
    #                  action="voter_added",
    #                  target_type="user",
    #                  target_id=str(user.id))
    # session.add(audit)
    # await session.commit()
    return voter


@router.delete("/voters/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_voter(student_id: str,
                       session: AsyncSession = Depends(get_async_session),
                       admin=Depends(admin_service.get_admin_user)):
    _ = await voter_service.delete_voter(student_id, session)
    # audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
    #                  action="voter_removed", target_type="user",
    #                  target_id=str(user.id))
    # session.add(audit)
    # await session.commit()
    return


@router.post("/elections/{election_id}/toggle")
async def toggle_election_publishing(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    election = await election_service.toggle_election_status(
        election_id, session
    )
    # audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
    #                  action="election_toggled", target_type="election",
    #                  target_id=str(election.id))
    # session.add(audit)
    # await session.commit()
    return {"is_published": election.is_published}


@router.get("/db/stats")
async def get_db_stats(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    # Return simple row counts per table
    from sqlalchemy import text

    tables_q = await session.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    )
    tables = [r[0] for r in tables_q.fetchall()]
    stats = {}
    for t in tables:
        q = text(f"SELECT count(*) FROM \"{t}\";")
        res = await session.execute(q)
        stats[t] = res.scalar()
    return {"stats": stats}
