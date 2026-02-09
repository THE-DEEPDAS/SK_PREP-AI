from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ================= APPLICATION =================
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key-here"

    # ================= DATABASE =================
    DATABASE_URL: str = "postgresql://admin:secure_password@localhost:5432/upsc_chatbot"
    REDIS_URL: str = "redis://localhost:6379"

    # ================= VECTOR DB =================
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # ================= LLM PROVIDER =================
    # openrouter | openai | local
    LLM_PROVIDER: str = "openrouter"

    # ---------- OpenRouter ----------
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_EMBED_MODEL: str = "text-embedding-3-large"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # ---------- Local GGUF (optional) ----------
    LOCAL_MODEL_PATH: Optional[str] = None

    # ---------- OpenAI (direct) ----------
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # ================= MISC =================
    DEFAULT_MODEL: str = "mistral"

    class Config:
        env_file = ".env"


settings = Settings()
