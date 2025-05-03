import logging
from typing import Sequence

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

    with get_http_client(settings) as http_client, get_db_session() as db_session:
        pending_addresses = get_pending_addresses(db_session)

        for address in pending_addresses[:2]:
            process_address_wrapper(address, transformer, http_client, db_session)


def get_pending_addresses(db_session: Session) -> Sequence[Address]:
    result = db_session.execute(select(Address).where(Address.status == "pending"))
    addresses = result.scalars().all()

    if not addresses:
        logger.info("No pending addresses")

    return addresses


def process_address_wrapper(
    address: Address,
    transformer: StreetEasyTransformer,
    http_client: httpx.Client,
    db_session: Session,
) -> None:
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
    # Turn input_address to url
    url = input_address_to_url(address.input_address, settings.STREETEASY_BASE_URL)
    address.streeteasy_url = url

    # Extract streeteasy html
    response = http_client.get(url)
    response.raise_for_status()

    # Transform and load streeteasy html
    transformer.update_address(response.text, address)
    db_session.commit()


if __name__ == "__main__":
    run_sync_pipeline()
