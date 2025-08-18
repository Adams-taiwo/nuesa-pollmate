from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.session import get_async_session
from ...models.student import User
from ...core.auth_utils import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ...schemas.student import StudentLogin

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login_students(
    login_data: StudentLogin,
    session: AsyncSession = Depends(get_async_session)
):
    student_id = login_data.student_id
    matric_number = login_data.matric_number

    statement = select(User).where(
        User.student_id == student_id
    )
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid student ID"
        )
    else:
        if matric_number != user.matric_number:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid matriculation number"
            )

    access_token = create_access_token(
        user_data={
            "matric_number": user.matric_number,
            "student_id": user.student_id
        },
        expiry=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_access_token(
        user_data={"matric_number": user.matric_number,
                   "student_id": user.student_id},
        expiry=timedelta(hours=8),
        refresh=True
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "student_id": user.student_id,
                "matric_number": user.matric_number
            }
        }
    )
