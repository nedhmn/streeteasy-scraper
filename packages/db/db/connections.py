from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from db.config import settings

# Sync engine
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)
sync_db_session = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    session = sync_db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Async engine
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)
async_db_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
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
