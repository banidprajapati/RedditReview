from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str = Field(..., description="Reddit Client ID")
    REDDIT_CLIENT_SECRET: str = Field(..., description="Reddit Client Secret")
    REDDIT_USER_AGENT: str = Field(..., description="Reddit User Agent")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Easier for Docker/Kubernetes environments
        extra="ignore",  # Ignore unexpected env vars
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
