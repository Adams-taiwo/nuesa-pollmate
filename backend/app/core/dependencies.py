from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import get_async_session
from ..models.student import User
from ..core.auth_utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload: dict | None = decode_token(token)
    matric_number = None
    if payload is not None:
        matric_number = payload.get("sub")

        if matric_number is None:
            raise credentials_exception

        user = await session.execute(
            select(User).where(User.matric_number == matric_number)
        )
        user = user.scalar_one_or_none()

        if user is None:
            raise credentials_exception
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        return user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Check if the current user is an admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have adequate privileges"
        )
    return current_user


class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> dict | None:
        creds = await super().__call__(request=request)

        if creds is not None:
            token = creds.credentials

            if not self.validate_token(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invaild token passed"
                )
            
            token_data = decode_token(token)

            self.verify_token_data(token_data)

            return token_data
        

    def verify_token_data(self, token_data) -> None:
        raise NotImplementedError("Override this method in child class")


    def validate_token(self, token: str) -> bool:
        token_data = decode_token(token=token)

        return True if token_data is not None else False
    

class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        print(token_data)
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Enter a valid access token"
            )
