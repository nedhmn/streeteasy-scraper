import asyncio
import logging

from utils.logging import setup_logger

from db.db import async_engine
from db.models import Base

setup_logger()
logger = logging.getLogger("db.main")


async def init_db() -> None:
    async with async_engine.begin() as conn:
        logger.info("Attempting to create all database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created or already exist.")


if __name__ == "__main__":
    asyncio.run(init_db())
