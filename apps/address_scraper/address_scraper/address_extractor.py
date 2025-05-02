import io
import re

import bs4
import httpx
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from address_scraper.config import Settings


class AddressExtractor:
    """Extracts addresses from nyc.gov class b dwelling list."""

    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient,
        db_session: AsyncSession,
    ) -> None:
        self.settings = settings
        self.http_client = http_client
        self.db_session = db_session

    async def run(self) -> list[str]:
        xls_url = await self._get_xls_download_url()
        addresses = await self._get_addresses_from_xls(xls_url)

        return addresses

    async def _get_xls_download_url(self) -> str:
        # Get request to classb listings url
        response = await self.http_client.get(self.settings.NYC_GOV_CLASSB_URL)
        response.raise_for_status()

        # Anchor tag pattern to find xls url
        pattern = re.compile(
            r"^/assets/specialenforcement/downloads/excel/class-b-multiple-dwelling-list-amended-\d{2}-\d{2}-\d{2}\.xlsx$"
        )

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        xls_link_tag = soup.find("a", href=pattern)

        if not xls_link_tag:
            raise Exception("NYC ClassB Dwelling XLS URL not found.")

        return f"{self.settings.NYC_GOV_URL}/{xls_link_tag.get('href')}"

    async def _get_addresses_from_xls(self, xls_url: str) -> list[str]:
        # Download xls content
        response = await self.http_client.get(xls_url)
        response.raise_for_status()

        # Read data in memory
        xls_data = io.BytesIO(response.content)

        # Read excel and parse addresses
        xls_df = pd.read_excel(xls_data, skiprows=5)
        addresses = (
            xls_df.query("Borough in @self.settings.BOROUGHS_TO_KEEP")
            .sort_values("Combined Address")["Combined Address"]
            .tolist()
        )

        if not addresses:
            raise Exception("No addresses found in XLS.")

        return addresses
