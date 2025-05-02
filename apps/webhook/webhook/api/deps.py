from typing import Annotated

from db.connections import get_async_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DbSessionDep = Annotated[AsyncSession, Depends(get_async_db_session)]
