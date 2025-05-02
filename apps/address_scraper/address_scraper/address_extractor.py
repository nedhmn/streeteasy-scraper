from address_scraper.config import Settings


class AddressExtractor:
    """Extracts addresses from nyc.gov class b dwelling list."""

    def __init__(self, settings: Settings) -> None:
        pass

    async def run() -> list[str]:
        pass

    async def _get_xls_download_url(self) -> str:
        pass

    async def _get_addresses_from_xls(self) -> list[str]:
        pass
