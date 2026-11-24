"""App configuration: read from env vars (and a local .env file), validated at startup."""

from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Where values come from, highest priority first: real env vars → .env file → defaults below.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["local", "test", "staging", "production"] = "local"  # env var: APP_ENV
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"  # env var: LOG_LEVEL
    log_format: Literal["json", "console"] = "json"  # json for servers; console = readable locally

    @field_validator("log_level", mode="before")
    @classmethod
    def _uppercase(cls, value: object) -> object:
        # Accept LOG_LEVEL=debug as well as DEBUG (runs BEFORE the Literal check).
        return value.upper() if isinstance(value, str) else value


@lru_cache
def get_settings() -> Settings:
    """Read and validate config ONCE; every later call returns the same object."""
    return Settings()
