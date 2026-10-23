from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GST Invoice Intelligence"
    environment: str = "development"
    llm_provider: Literal["openai", "anthropic"] = "openai"
    openai_api_key: SecretStr = SecretStr("")
    anthropic_api_key: SecretStr = SecretStr("")
    anthropic_model: str = "claude-3-5-haiku-latest"
    llm_temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    max_extraction_attempts: int = Field(default=2, get=1, le=4)
    max_input_characters: int = Field(default=30000, ge=1000, le=100000)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()