from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc

from ...schemas import (admin as admin_schemas,
                        candidate as candidate_schemas,
                        election as election_schemas,
                        student as student_schemas,
                        vote as vote_schemas)
from ...db.session import get_async_session
from ...core.dependencies import AccessTokenBearer
from ...models.audit_log import AuditLog
from ...models.candidate import Candidate
from ...models.election import Election
from ...models.student import User, UserRole
from ...services import (admin_service,
                         audit_log_service,
                         election_service,
                         candidate_service,
                         voter_service)
from ...schemas.student import UserRead


router = APIRouter(prefix="/admin", tags=["admin"])

access_bearer = Depends(AccessTokenBearer())


@router.post("/create/admin",
             response_model=UserRead,
             status_code=status.HTTP_201_CREATED,
             dependencies=[access_bearer])
async def create_admin(
    payload: student_schemas.AdminCreateSchema,
    session: AsyncSession = Depends(get_async_session),
):
    new_admin = await admin_service.create_admin_user(payload, session)

    _ = await audit_log_service.create_audit_log(
        actor_id=new_admin.student_id,
        action="Admin Created",
        target_type="user",
        target_id=new_admin.student_id,
        session=session)

    return {
        "student_id": new_admin.student_id,
        "matric_number": new_admin.matric_number,
        "role": new_admin.role.value,
        "is_active": new_admin.is_active
    }


@router.get("/admins",
            dependencies=[access_bearer])
async def get_admins(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    statement = select(User).where(User.role == UserRole.admin,)
    results = await session.execute(statement)
    admins = results.scalars().all()
    return [
        {
            "student_id": admin.student_id,
            "matric_number": admin.matric_number,
            "role": admin.role.value,
            "is_active": admin.is_active
        }
        for admin in admins
    ]


@router.get("/all_elections",
            response_model=List[admin_schemas.ElectionCreateResponse])
async def get_all_elections(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    elections = []
    if admin.role == UserRole.admin:
        statement = select(Election).order_by(
            desc(Election.created_at)
        )
        results = await session.execute(statement)
        elections = results.scalars().all()

    return [
        admin_schemas.ElectionCreateResponse.model_validate(election) for election in elections
        ]


@router.post("/elections",
             response_model=election_schemas.ElectionRead,
             status_code=status.HTTP_201_CREATED)
async def create_election(
    payload: election_schemas.CreateElection,
    session: AsyncSession = Depends(get_async_session),
    _=Depends(admin_service.get_admin_user),
):
    election = await election_service.create_election(payload, session)

    _ = await audit_log_service.create_audit_log(
        actor_id=payload.created_by,
        action="election_created",
        target_type="election",
        target_id=str(election.id),
        session=session
    )

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

    _ = await audit_log_service.create_audit_log(
        actor_id=admin if hasattr(admin, "id") else "",
        action="election_updated",
        target_type="election",
        target_id=str(election.id),
        session=session
    )

    return election


@router.delete(
    "/elections/{election_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_election(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    if admin.role == UserRole.admin:
        del_election = await election_service.delete_election(election_id,
                                                              session)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this election"
        )

    _ = await audit_log_service.create_audit_log(
        actor_id=admin if hasattr(admin, "id") else "",
        action=f"""Election having title  of
         {del_election["election_title"]} Deleted""",
        target_type="election",
        target_id=str(election_id),
        session=session
    )

    return


@router.get("/audit/logs",
            response_model=List[admin_schemas.AuditLogReadSchema])
async def get_audit_logs(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    _=Depends(admin_service.get_admin_user),
):
    created_col = AuditLog.__table__.c.created_at
    statement = select(AuditLog).order_by(created_col.desc()).limit(limit).offset(offset)
    result = await session.execute(statement)
    logs = result.scalars().all()
    return admin_schemas.AuditLogAdapter.validate_python(logs)


@router.get("/candidates",
            response_model=List[candidate_schemas.CandidateCreateSchema])
async def get_all_candidates(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    candidates = []
    if admin.role == UserRole.admin:
        statement = select(Candidate).where(
            Candidate.created_at is not None
        )
        results = await session.execute(statement)
        candidates = results.scalars().all()

    return [
        candidate_schemas.CandidateRead.model_validate(candidate) for candidate in candidates
    ]


@router.post("/candidates", status_code=status.HTTP_201_CREATED)
async def add_candidate(
    payload: candidate_schemas.CandidateCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
  ):
    candidate = await candidate_service.create_candidate(
        payload, session
    )
    # _ = await audit_log_service.create_audit_log(
    #     actor_id=admin if hasattr(admin, "id") else "",
    #     action="Candidate Added",
    #     target_type="candidate",
    #     target_id=str(candidate.student_id),
    #     session=session
    #     )
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

    # _ = await audit_log_service.create_audit_log(
    #     actor_id=admin if hasattr(admin, "id") else "",
    #     action="Candidate Update",
    #     target_type="candidate",
    #     target_id=updated_candidate.student_id,
    #     session=session
    # )

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

    # _ = await audit_log_service.create_audit_log(
    #   actor_id=admin if hasattr(admin, "id") else "",
    #   action="Candidate Deleted",
    #   target_type="candidate",
    #   target_id=str(candidate_id),
    #   session=session)

    return


@router.post("/voters",
             status_code=status.HTTP_201_CREATED)
async def add_voter(payload: vote_schemas.VoteCreateSchema,
                    session: AsyncSession = Depends(get_async_session),
                    admin=Depends(admin_service.get_admin_user)):
    voter = await voter_service.create_voter(payload, session)

    # _ = await audit_log_service.create_audit_log(
    #     actor_id=admin if hasattr(admin, "id") else "",
    #     action="Voter Added",
    #     target_type="user",
    #     target_id=voter.student_id)

    return voter


@router.delete("/voters/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_voter(student_id: str,
                       voter_id: str,
                       session: AsyncSession = Depends(get_async_session),
                       admin=Depends(admin_service.get_admin_user)):
    _ = await voter_service.delete_voter(voter_id, session)

    # _ = await audit_log_service.create_audit_log(
    #     actor_id=admin if hasattr(admin, "id") else "",
    #     action="Voter Removed",
    #     target_type="user",
    #     target_id=student_id)
    return


@router.post("/elections/{election_id}/toggle",
             status_code=status.HTTP_201_CREATED)
async def toggle_election_publishing(
    election_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user)
):
    election = await election_service.toggle_election_status(
        election_id, session
    )

    _ = await audit_log_service.create_audit_log(
        actor_id=admin if hasattr(admin, "id") else "",
        action="Election State Toggled",
        target_type="election",
        target_id=str(election_id))

    return {"is_published": election.is_published}


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


@router.get("/db/stats")
async def get_db_stats(
    session: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_service.get_admin_user),
):
    from sqlalchemy import text

    tables_q = await session.execute(
        text("""
             SELECT table_name FROM information_schema.tables
              WHERE table_schema='public';""")
    )
    tables = [r[0] for r in tables_q.fetchall()]
    stats = {}
    for t in tables:
        q = text(f"SELECT count(*) FROM \"{t}\";")
        res = await session.execute(q)
        stats[t] = res.scalar()
    return {"stats": stats}
