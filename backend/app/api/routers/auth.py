from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    generate_salt,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ...db.session import get_async_session
from ...models.user import User, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register")
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Register a new user."""
    # Check if user already exists
    query = select(User).where(
        (User.matric_number == user_data.matric_number) |
        (User.student_id == user_data.student_id)
    )
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this matric number or student ID already exists"
        )

    # Generate salt and hash password
    salt = generate_salt()
    hashed_password = hash_password(user_data.password, salt)

    # Create new user
    user = User(
        matric_number=user_data.matric_number,
        student_id=user_data.student_id,
        role=user_data.role,
        hashed_password=hashed_password,
        salt=salt
    )

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "message": "User registered successfully",
        "user_id": str(user.id)
    }


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    """Login user and return JWT token."""
    # Find user by matric number (which serves as username)
    query = select(User).where(User.matric_number == form_data.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect matric number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.salt, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect matric number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.matric_number, "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login/custom")
async def login_with_credentials(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """Custom login endpoint that accepts both matric number and student ID."""
    # Find user by both matric number and student ID
    query = select(User).where(
        (User.matric_number == credentials.matric_number) &
        (User.student_id == credentials.student_id)
    )
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(credentials.password, user.salt, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.matric_number,
            "role": user.role,
            "student_id": user.student_id
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "matric_number": user.matric_number,
            "student_id": user.student_id,
            "role": user.role
        }
    }


@router.post("/refresh")
async def refresh_token(
    current_token: str = Depends(OAuth2PasswordRequestForm),
    session: AsyncSession = Depends(get_async_session)
):
    """Refresh an existing valid token."""
    try:
        # Verify current token and get user info
        from ...core.auth_utils import verify_token
        payload = verify_token(current_token)
        matric_number = payload.get("sub")

        if not matric_number:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Get user from database
        query = select(User).where(User.matric_number == matric_number)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.matric_number, "role": user.role},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
