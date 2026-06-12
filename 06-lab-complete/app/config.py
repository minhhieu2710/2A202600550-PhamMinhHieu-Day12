from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PORT: int = 8000
    REDIS_URL: str = "redis://localhost:6379/0"
    AGENT_API_KEY: str = "default-secret-key"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_PER_MINUTE: int = 10
    MONTHLY_BUDGET_USD: float = 10.0
    MODEL_NAME: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"

settings = Settings()