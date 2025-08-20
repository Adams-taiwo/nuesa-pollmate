from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
import uuid
from ..models.audit_log import AuditLog
from ..db.session import get_async_session
from ..schemas.audit_log import (AuditLogCreateSchema,
                                 AuditLogRead)


async def create_audit_log(
    actor_id: str | None,
    action: str,
    target_type: str,
    target_id: uuid.UUID | str,
    metadata=None,
    session: AsyncSession = Depends(get_async_session)
):
    if metadata is None:
        metadata = {}

    audit_log = AuditLog(
        actor_student_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
    )

    session.add(audit_log)
    
    try:
        await session.commit()
        await session.refresh(audit_log)
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return audit_log
