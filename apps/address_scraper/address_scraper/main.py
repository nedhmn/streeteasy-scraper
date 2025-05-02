import asyncio
import logging

import httpx
from db.connections import get_async_db_session
from db.models import Address
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logging import setup_logger

from address_scraper.address_extractor import AddressExtractor
from address_scraper.config import settings

setup_logger("address_scraper.log")
logger = logging.getLogger("address_scraper.main")


async def main() -> None:
    logger.info("Starting address scraping process.")
    async with httpx.AsyncClient() as http_client, get_async_db_session() as db_session:
        # Extract addresses
        logger.info("Extracting addresses from source.")
        extractor = AddressExtractor(settings, http_client, db_session)
        input_addresses = await extractor.run()
        logger.info("Extracted %s addresses.", len(input_addresses))

        # Load addresses to database
        logger.info("Loading addresses to database.")
        await load_addresses_to_db(input_addresses, db_session)
        logger.info("Addresses loaded to database successfully.")


async def load_addresses_to_db(
    input_addresses: list[str], db_session: AsyncSession
) -> None:
    addresses = [
        Address(input_address=input_address) for input_address in input_addresses
    ]

    db_session.add_all(addresses)
    await db_session.commit()


if __name__ == "__main__":
    asyncio.run(main())
