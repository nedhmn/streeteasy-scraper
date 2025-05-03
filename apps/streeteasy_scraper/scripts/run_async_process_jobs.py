import asyncio
import logging
from typing import Sequence

import aiometer
import httpx
from db.connections import get_async_db_session
from db.models import Address
from streeteasy_scraper.asynchronous.job_result_extractor import JobResultExtractor
from streeteasy_scraper.common.streeteasy_transformer import StreetEasyTransformer
from streeteasy_scraper.common.utils import input_address_to_url
from streeteasy_scraper.config import settings
from utils.logging import setup_logger

setup_logger("run_async_process_jobs.log")
logger = logging.getLogger("scripts.run_async_process_jobs")


async def main() -> None:
    # Loop until no available jobs, then find "ready_to_process" jobs, then process them
    pass


async def has_available_jobs() -> bool:
    # Confirm jobs with statuses "sent_to_process" and "ready_to_process"
    pass


async def get_ready_to_process_jobs() -> Sequence[Address]:
    # Return jobs with status "ready_to_process", batch by 300 jobs
    pass


async def process_job() -> None:
    # Fetch job results

    # Transform results

    # Load to database
    pass


if __name__ == "__main__":
    asyncio.run(main())
