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
from streeteasy_scraper.asynchronous.job_result_extractor import JobResultExtractor
from streeteasy_scraper.common.streeteasy_transformer import StreetEasyTransformer
from streeteasy_scraper.config import settings
from utils.logging import setup_logger

setup_logger("run_async_process_jobs.log")
logger = logging.getLogger("scripts.run_async_process_jobs")


async def main() -> None:
    async with httpx.AsyncClient() as http_client:
        # Initialize extractor and transformer
        job_result_extractor = JobResultExtractor(settings, http_client)
        streeteasy_transformer = StreetEasyTransformer(settings)

        # Run process jobs
        while True:
            async with get_async_db_session() as db_session:
                # Checks if there are available jobs to continue script
                if not has_available_jobs(db_session):
                    logger.info("No more available jobs! Exiting...")
                    return

                # Get "ready_to_process" job ids
                address_ids = await get_ready_to_process_address_ids(db_session)
                if not address_ids:
                    logger.info("No jobs are ready_to_process yet.")
                    await asyncio.sleep(settings.PROCESS_JOBS_SLEEP_INTERVAL)
                    continue

            # Process jobs
            await aiometer.run_on_each(
                async_fn=functools.partial(
                    process_address,
                    job_result_extractor=job_result_extractor,
                    streeteasy_transformer=streeteasy_transformer,
                ),
                args=address_ids,
                max_at_once=settings.AIOMETER_MAX_AT_ONCE,
                max_per_second=settings.AIOMETER_MAX_PER_SECOND,
            )

            # Sleep until next run
            await asyncio.sleep(settings.PROCESS_JOBS_SLEEP_INTERVAL)


async def has_available_jobs(db_session: AsyncSession) -> bool:
    result = await db_session.execute(
        select(Address.id)
        .where(Address.status.in_(["sent_to_process", "ready_to_process"]))
        .limit(1)
    )
    return result.first() is not None


async def get_ready_to_process_address_ids(db_session: AsyncSession) -> Sequence[UUID]:
    result = await db_session.execute(
        select(Address.id)
        .where(Address.status == "ready_to_process")
        .limit(settings.PROCESS_JOBS_BATCH_SIZE)
    )
    return result.scalars().all()


async def process_address(
    address_id: UUID,
    job_result_extractor: JobResultExtractor,
    streeteasy_transformer: StreetEasyTransformer,
) -> None:
    async with get_async_db_session() as db_session:
        # Get address instance
        address = await db_session.get(Address, address_id)
        if not address:
            logger.error("Address with ID %s not found.", address_id)
            return

        # Get address data
        assert isinstance(address.brightdata_response_id, str)
        address_data = await job_result_extractor.run(address.brightdata_response_id)

        # Update address with processed data
        if address_data:
            streeteasy_transformer.update_address(address_data, address)
        else:
            logger.warning("Address with ID %s has no HTMl data.", address_id)
            address.status = "failed"

        await db_session.commit()


if __name__ == "__main__":
    asyncio.run(main())
