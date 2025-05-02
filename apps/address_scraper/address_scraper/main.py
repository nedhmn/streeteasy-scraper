import asyncio

import httpx
from db.connections import get_async_db_session

from address_scraper.address_extractor import AddressExtractor
from address_scraper.config import settings


async def main():
    async with httpx.AsyncClient() as http_client, get_async_db_session() as db_session:
        extractor = AddressExtractor(settings, http_client, db_session)
        addresses = await extractor.run()
        print(addresses[:5])


if __name__ == "__main__":
    asyncio.run(main())
