from datetime import datetime, timedelta, timezone
from jose import exceptions
import jwt
from fastapi import HTTPException, status
from typing import Optional
from .config import Config
import uuid


ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_data: dict,
                        expiry: Optional[timedelta] = None,
                        refresh: bool = False) -> str:
    payload = {}

    payload['user'] = user_data
    if expiry:
        payload['exp'] = datetime.now(timezone.utc) + expiry
    else:
        payload['exp'] = (datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
