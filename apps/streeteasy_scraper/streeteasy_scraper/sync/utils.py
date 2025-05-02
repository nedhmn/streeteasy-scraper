import httpx
from streeteasy_scraper.config import Settings


def get_http_client(settings: Settings) -> httpx.Client:
    mounts = {
        "http://": settings.BRIGHTDATA_PROXY_URL,
        "https://": settings.BRIGHTDATA_PROXY_URL,
    }

    return httpx.Client(
        http_client=httpx.Client(
            mounts=mounts,
            timeout=settings.HTTP_TIMEOUT,
            follow_redirects=True,
            verify=False,
        )
    )
