from pydantic import BaseModel, Field


class Settings(BaseModel):
    TITLE: str = Field(default="StreetEasy Scraper API")
    API_V1_PREFIX: str = Field(default="/api/v1")


settings = Settings()
