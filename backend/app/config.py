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
    # ollama | local | openai
    LLM_PROVIDER: str = "openai"

    # ---------- Ollama ----------
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "upsc-mistral"

    # ---------- Local GGUF ----------
    LOCAL_MODEL_PATH: Optional[str] = None

    # ---------- OpenAI ----------
    OPENAI_API_KEY: Optional[str] = None

    # ================= MISC =================
    DEFAULT_MODEL: str = "mistral"

    class Config:
        env_file = ".env"


settings = Settings()
