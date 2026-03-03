from fastapi import HTTPException, status
import jwt
from logging import Logger
from datetime import datetime, timedelta, timezone
from typing import Optional
from .config import Config
import uuid


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRY_MINUTES = 300


logger = Logger("logger")

def create_access_token(user_data: dict,
                        expiry: Optional[timedelta] = None) -> str:
    payload = {}

    payload['user'] = user_data
    if expiry:
        payload['exp'] = datetime.now(timezone.utc) + expiry
    else:
        payload['exp'] = (datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = False

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


# This might be completely unecessary
def create_refresh_token(user_data: dict,
                        expiry: Optional[timedelta] = None) -> str:
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now(timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRY_MINUTES)
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = True

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data

    except jwt.PyJWTError as e:
        logger.exception(e)

        return None
