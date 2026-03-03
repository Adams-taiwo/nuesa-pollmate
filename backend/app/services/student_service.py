from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from ..db.session import get_async_session
from ..models.student import User
from ..schemas.student import UserCreateSchema


async def get_user(
        student_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(User.student_id == student_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student having that id not found"
        )

    return user


async def create_student(
        user_data: UserCreateSchema,
        session: AsyncSession = Depends(get_async_session)
):
    student = User(**user_data.model_dump())

    statement = select(User).where(User.student_id == user_data.student_id)
    result = await session.execute(statement)
    exists = result.scalar_one_or_none()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that student id already exists"
        )
    
    session.add(student)
    await session.commit()
    await session.refresh(student)

    return student


async def delete_student(
        student_id,
        session: AsyncSession = Depends(get_async_session)
        ):
    student_to_delete = await get_user(student_id, session)

    await session.delete(student_to_delete)
    await session.commit()

    return {"message": f"Student have student id of {student_id} deleted"}
