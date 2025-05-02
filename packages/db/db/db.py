from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.config import settings

async_engine = create_async_engine(settings.DATABASE_URL)
async_db_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronous database session context manager"""
    session = async_db_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
