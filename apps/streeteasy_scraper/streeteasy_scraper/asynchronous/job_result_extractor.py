import httpx

from streeteasy_scraper.config import Settings


class JobResultExtractor:
    def __init__(self, settings: Settings, http_client: httpx.AsyncClient) -> None:
        self.settings = settings
        self.http_client = http_client
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BRIGHTDATA_API_TOKEN}",
        }

    async def run(self, response_id: str) -> str | None:
        url = (
            f"{self.settings.BRIGHTDATA_GET_RESULT_BASE_URL}&response_id={response_id}"
        )

        # Get response id data
        response = await self.http_client.get(url=url, headers=self.headers)
        response.raise_for_status()

        html = response.text.strip()

        if not html.startswith("<!DOCTYPE html>"):
            return None

        return html
