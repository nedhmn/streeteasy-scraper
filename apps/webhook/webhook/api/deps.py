from typing import Annotated, AsyncGenerator

from db.connections import async_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_session() as db_session:
        yield db_session


DbSessionDep = Annotated[AsyncSession, Depends(get_async_db_session)]
