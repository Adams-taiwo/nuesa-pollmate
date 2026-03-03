from fastapi import APIRouter
from sqlalchemy.ext.asyncio.session import AsyncSession
from ...db.session import get_async_session


router = APIRouter(prefix="")
