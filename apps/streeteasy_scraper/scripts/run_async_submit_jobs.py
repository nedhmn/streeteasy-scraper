import asyncio
import logging
from typing import Sequence

import httpx
from db.connections import get_async_db_session
from db.models import Address
from streeteasy_scraper.asynchronous.job_submitter import JobSubmitter
from streeteasy_scraper.config import settings
from utils.logging import setup_logger

setup_logger("run_async_pipeline.log")
logger = logging.getLogger("run_async_submit_jobs")


async def run_async_submit_jobs() -> None:
    pass


async def get_pending_addresses() -> Sequence[Address]:
    pass


async def update_job_status_in_db() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(run_async_submit_jobs())
