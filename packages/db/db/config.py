from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: Literal["local", "production"] = Field(default="local")
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        # Set host to localhost if enviornment is local
        host = "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST

        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{host}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
