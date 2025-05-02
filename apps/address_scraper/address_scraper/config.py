from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    NYC_GOV_CLASSB_URL: str = Field(
        default="https://www.nyc.gov/site/specialenforcement/reporting-law/class-b-mdl.page",
        description="Class B multiple dwellings list URL.",
    )
    NYC_GOV_URL: str = Field(default="https://www.nyc.gov/")
    STREETEASY_BASE_URL: str = Field(default="https://streeteasy.com/search")
    BOROUGHS_TO_KEEP: Annotated[list[str], NoDecode] = Field(
        default="MANHATTAN",  # type: ignore
        description="Boroughs to keep when saving addresses to database.",
    )

    # Set roles in env as csv and parse as list
    # ref: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#disabling-json-parsing
    @field_validator("BOROUGHS_TO_KEEP", mode="before")
    @classmethod
    def parse_csv_to_list(cls, boroughs: str) -> list[str]:
        return [borough for borough in boroughs.split(",")]


settings = Settings()
