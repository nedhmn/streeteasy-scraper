import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Sequence
from uuid import UUID

import httpx
from db.connections import get_db_session
from db.models import Address
from sqlalchemy import select
from sqlalchemy.orm import Session
from streeteasy_scraper.common.streeteasy_transformer import StreetEasyTransformer
from streeteasy_scraper.config import settings
from streeteasy_scraper.sync.utils import get_http_client, input_address_to_url
from tenacity import (
    RetryError,
    after_log,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)
from utils.logging import setup_logger

setup_logger("run_sync_pipeline.log")
logger = logging.getLogger("streeteasy_scraper.run_sync_pipeline")


def run_sync_pipeline():
    transformer = StreetEasyTransformer(settings)

    with get_http_client(settings) as http_client:
        # Get pending addresses id
        with get_db_session() as session:
            pending_addresses_id = get_pending_addresses_id(session)

        with ThreadPoolExecutor(
            max_workers=settings.THREADPOOL_MAX_WORKERS
        ) as executor:
            # Create list of futures
            futures = [
                executor.submit(
                    process_address_wrapper, address_id, transformer, http_client
                )
                for address_id in pending_addresses_id[:2]
            ]

            # Process address
            for future in as_completed(futures):
                future.result()


def get_pending_addresses_id(db_session: Session) -> Sequence[UUID]:
    result = db_session.execute(select(Address.id).where(Address.status == "pending"))
    addresses = result.scalars().all()

    if not addresses:
        logger.info("No pending addresses")

    return addresses


def process_address_wrapper(
    address_id: UUID,
    transformer: StreetEasyTransformer,
    http_client: httpx.Client,
):
    with get_db_session() as db_session:
        address = db_session.get(Address, address_id)
        if not address:
            logger.error("Address with id %s not found.", address_id)
            return

        try:
            process_address(address, transformer, http_client, db_session)
        except RetryError:
            address.status = "failed"
            db_session.commit()


@retry(
    stop=stop_after_attempt(settings.TENACITY_STOP_AFTER_ATTEMPT),
    wait=wait_fixed(settings.TENACITY_WAIT_FIXED),
    retry=retry_if_exception_type(httpx.HTTPStatusError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO),
)
def process_address(
    address: Address,
    transformer: StreetEasyTransformer,
    http_client: httpx.Client,
    db_session: Session,
) -> None:
    # Create URL and update the address instance accordingly.
    url = input_address_to_url(address.input_address, settings.STREETEASY_BASE_URL)
    address.streeteasy_url = url

    # Extract StreetEasy HTML.
    response = http_client.get(url)
    response.raise_for_status()

    # Transform and load StreetEasy HTML.
    transformer.update_address(response.text, address)
    db_session.commit()


if __name__ == "__main__":
    run_sync_pipeline()
