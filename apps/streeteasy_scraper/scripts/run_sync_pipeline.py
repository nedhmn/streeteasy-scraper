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

# Setup logger
setup_logger("run_sync_pipeline.log")
logger = logging.getLogger("run_sync_pipeline")


def run_sync_pipeline() -> None:
    logger.info("Starting sync pipeline")
    transformer = StreetEasyTransformer(settings)

    with get_http_client(settings) as http_client:
        with get_db_session() as session:
            pending_addresses_id = get_pending_addresses_id(session)

        if not pending_addresses_id:
            logger.info("No pending addresses found. Exiting.")
            return

        consecutive_error_count = 0

        with ThreadPoolExecutor(
            max_workers=settings.THREADPOOL_MAX_WORKERS
        ) as executor:
            logger.info("Processing %d pending addresses", len(pending_addresses_id))

            futures = [
                executor.submit(
                    process_address_wrapper, address_id, transformer, http_client
                )
                for address_id in pending_addresses_id
            ]

            for future in as_completed(futures):
                success = future.result()

                if not success:
                    consecutive_error_count += 1
                    logger.warning(
                        "Address processing failed. Consecutive errors: %d/%d",
                        consecutive_error_count,
                        settings.CONSECUTIVE_ERROR_MAX,
                    )
                    if consecutive_error_count >= settings.CONSECUTIVE_ERROR_MAX:
                        logger.critical(
                            "%d consecutive errors met. Exiting script.",
                            settings.CONSECUTIVE_ERROR_MAX,
                        )
                        raise Exception(
                            f"{settings.CONSECUTIVE_ERROR_MAX} consecutive errors met. Exiting script.",
                        )
                else:
                    consecutive_error_count = 0


def get_pending_addresses_id(db_session: Session) -> Sequence[UUID]:
    logger.info("Fetching pending addresses from database")
    result = db_session.execute(select(Address.id).where(Address.status == "pending"))
    addresses = result.scalars().all()

    return addresses


def process_address_wrapper(
    address_id: UUID,
    transformer: StreetEasyTransformer,
    http_client: httpx.Client,
) -> bool:
    """process_address wrapper to catch tenacity's RetryError and return process status"""
    logger.info("Processing address ID: %s", address_id)
    with get_db_session() as db_session:
        address = db_session.get(Address, address_id)
        if not address:
            logger.error("Address with ID %s not found.", address_id)
            return True

        try:
            process_address(address, transformer, http_client, db_session)
            logger.info("Successfully processed address ID: %s", address_id)
            return True
        except RetryError:
            logger.error("Failed to process address ID %s after retries", address_id)
            address.status = "failed"
            db_session.commit()
            return False


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
    url = input_address_to_url(address.input_address, settings.STREETEASY_BASE_URL)
    address.streeteasy_url = url

    response = http_client.get(url)
    response.raise_for_status()

    transformer.update_address(response.text, address)
    db_session.commit()


if __name__ == "__main__":
    run_sync_pipeline()
