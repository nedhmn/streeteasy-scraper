from pydantic import BaseModel, Field


class Settings(BaseModel):
    TITLE: str = Field(default="StreetEasy Scraper API")


settings = Settings()
