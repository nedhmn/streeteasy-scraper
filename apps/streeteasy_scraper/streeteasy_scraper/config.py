import httpx
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    BRIGHTDATA_USERNAME: str = Field(description="BrightData Web Unlocker API username")
    BRIGHTDATA_PASSWORD: str = Field(description="BrightData Web Unlocker API password")
    BRIGHTDATA_HOST: str = Field(description="BrightData Web Unlocker API host name")

    @property
    def BRIGHTDATA_PROXY_URL(self) -> httpx.HTTPTransport:
        return httpx.HTTPTransport(
            proxy=(
                f"http://{self.BRIGHTDATA_USERNAME}:"
                f"{self.BRIGHTDATA_PASSWORD}@"
                f"{self.BRIGHTDATA_HOST}"
            ),
            verify=False,
        )

    BRIGHTDATA_API_TOKEN: str = Field(description="BrightData Web Unlocker API token")
    BRIGHTDATA_CUSTOMER_ID: str = Field(
        description="BrightData Web Unlocker API customer ID"
    )
    BRIGHTDATA_ZONE: str = Field(description="BrightData Web Unlocker API zone")

    # Sync settings
    CONSECUTIVE_ERROR_MAX: int = Field(
        default=10,
        description="The maximum number of consecutive errors until script exits",
    )
    HTTP_TIMEOUT: int = Field(default=30, description="Http client timeout in seconds")
    THREADPOOL_MAX_WORKERS: int = Field(
        default=30, description="ThreadPoolExecutor max workers"
    )
    TENACITY_STOP_AFTER_ATTEMPT: int = Field(
        default=3, description="Sync pipeline tenacity stop retries after attempt"
    )
    TENACITY_WAIT_FIXED: int = Field(
        default=3, description="Sync pipeline tenacity retry wait time in seconds"
    )
    STREETEASY_BASE_URL: str = Field(default="https://streeteasy.com/search")
    NO_RESULTS_PATTERNS: list[str] = Field(
        default=[
            "no results found",
            "we couldn't find any matches",
            "try searching in a different area",
            "there were no matches for",
            "no units available. check back soon.",
        ],
        description="When scraping StreetEasy, if a page matches any of these patterns then there were no results found",
    )

    # Async settings
    AIOMETER_MAX_AT_ONCE: int = Field(default=100)
    AIOMETER_MAX_PER_SECOND: int = Field(default=30)
    PROCESS_JOBS_BATCH_SIZE: int = Field(default=300)
    PROCESS_JOBS_SLEEP_INTERVAL: int = Field(
        default=30, description="Process jobs sleep interval in seconds"
    )

    @property
    def BRIGHTDATA_SUBMIT_JOB_URL(self) -> str:
        return (
            "https://api.brightdata.com/unblocker/req?"
            f"customer={settings.BRIGHTDATA_CUSTOMER_ID}&"
            f"zone={settings.BRIGHTDATA_ZONE}"
        )

    @property
    def BRIGHTDATA_GET_RESULT_BASE_URL(self) -> str:
        return (
            "https://api.brightdata.com/unblocker/get_result"
            f"?customer={self.BRIGHTDATA_CUSTOMER_ID}"
            f"&zone={self.BRIGHTDATA_ZONE}"
        )


settings = Settings()
