"""Configuration management for AgentCore."""

import os
from functools import lru_cache

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


def _env_str(name: str, default: str) -> str:
    """Read string environment value."""
    return os.getenv(name, default)


def _env_int(name: str, default: int) -> int:
    """Read integer environment value."""
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    """Read boolean environment value."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Database
        self.database_url = _env_str("DATABASE_URL", "sqlite:///./agentcore.db")
        self.sqlalchemy_echo = _env_bool("SQLALCHEMY_ECHO", False)

        # Ollama LLM
        self.ollama_url = _env_str("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.llm_model = _env_str("LLM_MODEL", "mistral")
        self.llm_timeout = _env_int("LLM_TIMEOUT", 60)

        # Model paths
        self.model_path = _env_str("MODEL_PATH", "./models/router_model.pkl")
        self.model_signature_path = _env_str("MODEL_SIGNATURE_PATH", "./models/router_model.pkl.sig")

        # Security
        self.jwt_secret_key = _env_str("JWT_SECRET_KEY", "change-me-to-random-32-chars-minimum")
        self.jwt_algorithm = _env_str("JWT_ALGORITHM", "HS256")
        self.jwt_expiration_hours = _env_int("JWT_EXPIRATION_HOURS", 24)
        self.api_key = _env_str("API_KEY", "")

        # API Configuration
        self.api_workers = _env_int("API_WORKERS", 4)
        self.api_host = _env_str("API_HOST", "0.0.0.0")
        self.api_port = _env_int("API_PORT", 8000)

        # Logging
        self.log_level = _env_str("LOG_LEVEL", "INFO")
        self.log_file = _env_str("LOG_FILE", "logs/agentcore.log")

        # CORS
        self.allowed_origins = _env_str("ALLOWED_ORIGINS", "http://localhost:8000,http://localhost:8501")

        # Environment
        self.environment = _env_str("ENVIRONMENT", "development")
        self.app_debug = _env_bool("AGENTCORE_DEBUG", False)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# For quick access
settings = get_settings()
