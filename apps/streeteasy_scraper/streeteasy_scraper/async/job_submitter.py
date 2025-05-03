import httpx

from streeteasy_scraper.config import Settings


class JobSubmitter:
    def __init__(self, settings: Settings, http_client: httpx.AsyncClient):
        self.settings = settings
        self.http_client = http_client
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.BRIGHTDATA_API_TOKEN}",
        }

    async def run(self, url: str) -> str:
        # Submit job request to BrightData
        response = await self.http_client.post(
            url=self.settings.BRIGHTDATA_SUBMIT_JOB_URL,
            headers=self.headers,
            json={"url": url},
        )
        response.raise_for_status()

        # Return job's response id
        return response.headers["x-response-id"]
