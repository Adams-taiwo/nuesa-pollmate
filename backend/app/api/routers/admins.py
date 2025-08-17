from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from ...schemas import admin as admin_schemas
from ...db.session import get_async_session
from ...models.election import Election
from ...models.audit_log import AuditLog
from ...models.candidate import Candidate
from ...models.user import User
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])


async def get_admin_user():
    """Should return current user and check if they are an admin."""
    return None


@router.post("/elections", response_model=admin_schemas.ElectionCreateResponse)
async def create_election(
    payload: admin_schemas.ElectionCreatePayload,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
):
    # create election
    election = Election(
        title=payload.title,
        description=payload.description,
        start_time=payload.start_time,
        end_time=payload.end_time,
        created_by=payload.created_by,
    )
    session.add(election)
    await session.commit()
    await session.refresh(election)

    # log audit
    audit = AuditLog(
        actor_id=payload.created_by,
        action="election_created",
        target_type="election",
        target_id=str(election.id),
    )
    session.add(audit)
    await session.commit()

    return {
        "message": "Election created successfully",
        "election_id": str(election.id),
    }


@router.put("/elections/{election_id}")
async def update_election(
    election_id: UUID,
    payload: admin_schemas.ElectionUpdatePayload,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
):
    q = select(Election).where(Election.id == election_id)
    result = await session.execute(q)
    election = result.scalar_one_or_none()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    # allow updates only before start_time
    if election.start_time <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Cannot modify election after it has started",
        )

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(election, field, value)

    session.add(election)
    await session.commit()

    # audit log
    audit = AuditLog(
        actor_id=admin if hasattr(admin, "id") else None,
        action="election_updated",
        target_type="election",
        target_id=str(election.id),
    )
    session.add(audit)
    await session.commit()

    return {"message": "Election updated successfully"}


@router.delete(
    "/elections/{election_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_election(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
):
    q = select(Election).where(Election.id == election_id)
    result = await session.execute(q)
    election = result.scalar_one_or_none()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    if election.start_time <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Cannot delete an election that has already started",
        )
    await session.delete(election)
    await session.commit()

    # audit
    audit = AuditLog(
        actor_id=admin if hasattr(admin, "id") else None,
        action="election_deleted",
        target_type="election",
        target_id=str(election.id),
    )
    session.add(audit)
    await session.commit()

    return


@router.get("/audit/logs", response_model=List[admin_schemas.AuditLogRead])
async def get_audit_logs(
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
):
    # use table column to build order_by expression to avoid typing issues
    created_col = AuditLog.__table__.c.created_at
    q = select(AuditLog).order_by(created_col.desc()).limit(limit)
    result = await session.execute(q)
    logs = result.scalars().all()
    return [admin_schemas.AuditLogRead.from_orm(log) for log in logs]


@router.get("/db/schema")
async def get_db_schema(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
):
    # Return table names - dev-only utility
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
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user)
  ):
    """
      Minimal add candidate endpoint. Payload should include user_id
      and election_id and optional position/bio.
    """
    user_id = payload.get("user_id")
    election_id = payload.get("election_id")
    position = payload.get("position")
    bio = payload.get("bio")
    candidate = Candidate(
        user_id=user_id,
        election_id=election_id,
        position=position, bio=bio
        )
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)
    audit = AuditLog(
        actor_id=admin if hasattr(admin, "id") else None,
        action="candidate_added", target_type="candidate",
        target_id=str(candidate.id)
        )
    session.add(audit)
    await session.commit()
    return {"message": "Candidate added", "candidate_id": str(candidate.id)}


@router.put("/candidates/{candidate_id}")
async def update_candidate(
    candidate_id: UUID,
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user)
):
    q = select(Candidate).where(Candidate.id == candidate_id)
    res = await session.execute(q)
    candidate = res.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    for k, v in payload.items():
        setattr(candidate, k, v)
    session.add(candidate)
    await session.commit()
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="candidate_updated",
                     target_type="candidate",
                     target_id=str(candidate.id))
    session.add(audit)
    await session.commit()
    return {"message": "Candidate updated"}


@router.delete(
        "/candidates/{candidate_id}",
        status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user)
):
    q = select(Candidate).where(Candidate.id == candidate_id)
    res = await session.execute(q)
    candidate = res.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    await session.delete(candidate)
    await session.commit()
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="candidate_deleted",
                     target_type="candidate",
                     target_id=str(candidate.id))
    session.add(audit)
    await session.commit()
    return


@router.post("/voters")
async def add_voter(payload: dict,
                    session: AsyncSession = Depends(get_async_session),
                    admin=Depends(get_admin_user)):
    # Expected payload: matric_number, student_id (optional), role (optional)
    matric_number = payload.get("matric_number")
    student_id = payload.get("student_id")
    role = payload.get("role") or "student"
    user = User(matric_number=matric_number, student_id=student_id, role=role)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="voter_added",
                     target_type="user",
                     target_id=str(user.id))
    session.add(audit)
    await session.commit()
    return {"message": "Voter added", "user_id": str(user.id)}


@router.delete("/voters/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_voter(user_id: UUID,
                       session: AsyncSession = Depends(get_async_session),
                       admin=Depends(get_admin_user)):
    q = select(User).where(User.id == user_id)
    res = await session.execute(q)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="voter_removed", target_type="user",
                     target_id=str(user.id))
    session.add(audit)
    await session.commit()
    return


@router.post("/voters/import")
async def import_voters(file: bytes = Depends(),
                        session: AsyncSession = Depends(get_async_session),
                        admin=Depends(get_admin_user)):
    import csv
    from io import StringIO

    s = StringIO(file.decode("utf-8"))
    reader = csv.DictReader(s)
    added = []
    for row in reader:
        matric = row.get("matric_number")
        student_id = row.get("student_id") or None
        # basic validation for matric (e.g., 2022/1/90235)
        if matric and "/" in matric:
            user = User(matric_number=matric, student_id=student_id)
            session.add(user)
            await session.flush()
            added.append(str(user.id))
    await session.commit()
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="voters_imported",
                     target_type="user",
                     target_id=",".join(added))
    session.add(audit)
    await session.commit()
    return {"imported": len(added)}


@router.post("/elections/{election_id}/toggle")
async def toggle_election_publishing(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user)
):
    q = select(Election).where(Election.id == election_id)
    res = await session.execute(q)
    election = res.scalar_one_or_none()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    election.is_published = not bool(election.is_published)
    session.add(election)
    await session.commit()
    audit = AuditLog(actor_id=admin if hasattr(admin, "id") else None,
                     action="election_toggled", target_type="election",
                     target_id=str(election.id))
    session.add(audit)
    await session.commit()
    return {"is_published": election.is_published}


@router.get("/db/stats")
async def get_db_stats(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(get_admin_user),
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
