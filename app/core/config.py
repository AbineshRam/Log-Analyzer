from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Log Analyzer"
    ENV: str = "dev"
    DEBUG: bool = True

    # API
    API_PREFIX: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database (MongoDB)
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "log_analyzer"

    # LLM Provider
    LLM_PROVIDER: str = "ollama"
    # allowed: ollama | openai | llama

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # LLaMA (local / custom server)
    LLAMA_ENDPOINT: str | None = None
    LLAMA_MODEL: str | None = None

    # AI Behavior
    AI_TEMPERATURE: float = 0.2
    AI_MAX_TOKENS: int = 500

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()
