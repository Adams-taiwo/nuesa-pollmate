from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker
)
from sqlmodel import create_engine, SQLModel
from ..core.config import Settings

settings = Settings()

engine = AsyncEngine(
    create_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True
    )
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        from ..models.audit_log import AuditLog
        from ..models.candidate import Candidate
        from ..models.election import Election
        from ..models.student import User
        from ..models.vote import Vote


        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
