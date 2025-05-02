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
    BRIGHTDATA_API_TOKEN: str = Field(description="BrightData Web Unlocker API token")
    BRIGHTDATA_CUSTOMER_ID: str = Field(
        description="BrightData Web Unlocker API customer ID"
    )
    BRIGHTDATA_ZONE: str = Field(description="BrightData Web Unlocker API zone")


settings = Settings()
