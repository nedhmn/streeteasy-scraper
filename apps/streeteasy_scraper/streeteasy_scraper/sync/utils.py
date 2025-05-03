from urllib.parse import urlencode

import httpx
from streeteasy_scraper.config import Settings


def get_http_client(settings: Settings) -> httpx.Client:
    mounts = {
        "http://": settings.BRIGHTDATA_PROXY_URL,
        "https://": settings.BRIGHTDATA_PROXY_URL,
    }

    return httpx.Client(
        mounts=mounts,
        timeout=settings.HTTP_TIMEOUT,
        follow_redirects=True,
        verify=False,
    )


def input_address_to_url(input_address: str, streeteasy_base_url: str) -> str:
    encoded_params = urlencode({"utf8": "✓", "search": input_address, "commit": ""})
    return f"{streeteasy_base_url}?{encoded_params}"
