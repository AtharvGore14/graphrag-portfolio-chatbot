from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_api_key: str = ""
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "llama-3.1-8b-instant"
    llm_max_tokens: int = 300

    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme-neo4j-password"

    redis_url: str = "redis://redis:6379/0"

    mood_confidence_threshold: float = 0.5
    mood_model: str = "j-hartmann/emotion-english-distilroberta-base"
    chat_memory_max_turns: int = 10
    chat_memory_ttl_seconds: int = 86400


@lru_cache
def get_settings() -> Settings:
    return Settings()
