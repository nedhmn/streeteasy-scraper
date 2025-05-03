import asyncio
import functools
import logging
from typing import Sequence
from uuid import UUID

import aiometer
import httpx
from db.connections import get_async_db_session
from db.models import Address
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from streeteasy_scraper.asynchronous.job_submitter import JobSubmitter
from streeteasy_scraper.common.utils import input_address_to_url
from streeteasy_scraper.config import settings
from utils.logging import setup_logger

setup_logger("run_async_pipeline.log")
logger = logging.getLogger("run_async_submit_jobs")


async def run_async_submit_jobs() -> None:
    async with get_async_db_session() as db_session:
        pending_address_ids = await get_pending_address_ids(db_session)

    if not pending_address_ids:
        logger.info("No pending addresses.")
        return

    async with httpx.AsyncClient() as http_client:
        job_submitter = JobSubmitter(settings, http_client)

        await aiometer.run_on_each(
            async_fn=functools.partial(submit_job, job_submitter=job_submitter),
            args=pending_address_ids[:30],  # TODO: Remove subset when finished
            max_at_once=settings.AIOMETER_MAX_AT_ONCE,
            max_per_second=settings.AIOMETER_MAX_PER_SECOND,
        )


async def get_pending_address_ids(db_session: AsyncSession) -> Sequence[UUID]:
    result = await db_session.execute(
        select(Address.id).where(Address.status == "pending")
    )
    return result.scalars().all()


async def submit_job(address_id: int, job_submitter: JobSubmitter) -> None:
    async with get_async_db_session() as db_session:
        # Get address by id
        address = await db_session.get(Address, address_id)
        if not address:
            logger.error("Address with ID %s not found.", address_id)
            return

        # Create url with input_address
        url = input_address_to_url(address.input_address, settings.STREETEASY_BASE_URL)
        address.streeteasy_url = url

        # Submit job and get response_id
        response_id = await job_submitter.run(url)
        address.brightdata_response_id = response_id
        address.status = "sent_to_process"

        await db_session.commit()


if __name__ == "__main__":
    asyncio.run(run_async_submit_jobs())
