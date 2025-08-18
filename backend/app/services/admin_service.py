from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.session import get_async_session
from app.models.student import User, UserRole, UserCreate


async def get_admin_user(
    student_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    statement = select(User).where(User.student_id == student_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )

    return user

# async def create_admin_user(
#         user_data: UserCreate,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     user = User(**user_data.model_dump())
#     user.role = UserRole.admin

#     await session.add(user)
#     await session.commit()
#     await session.refresh(user)
