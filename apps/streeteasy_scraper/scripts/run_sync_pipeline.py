import httpx
from db.models import Address
from streeteasy_scraper.config import settings
from streeteasy_scraper.sync.utils import get_http_client


def run_sync_pipeline():
    with get_http_client(settings) as http_client:
        pass


def get_pending_jobs():
    pass


def process_jobs_wrapper():
    pass


def process_job():
    pass


if __name__ == "__main__":
    run_sync_pipeline()
