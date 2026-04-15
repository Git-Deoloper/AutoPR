"""LocalClaw configuration management"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _csv_env(name: str, default: List[str]) -> List[str]:
    """Read a comma-separated environment variable."""
    value = os.getenv(name)
    if value is None:
        return default

    items = [item.strip() for item in value.split(",")]
    return [item for item in items if item]


class Config:
    """Application configuration"""

    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama2")

    # Web UI
    WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
    WEB_PORT = int(os.getenv("WEB_PORT", 8000))
    WEB_DEBUG = os.getenv("WEB_DEBUG", "False").lower() == "true"
    WEB_ALLOWED_ORIGINS = _csv_env(
        "WEB_ALLOWED_ORIGINS",
        ["http://localhost:8000", "http://127.0.0.1:8000"],
    )
    WEB_ALLOW_CREDENTIALS = (
        os.getenv("WEB_ALLOW_CREDENTIALS", "False").lower() == "true"
    )
    WORKSPACE_ROOT = Path(
        os.getenv("WORKSPACE_ROOT", os.getcwd())
    ).expanduser().resolve()

    # File reading
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1048576))  # 1MB

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Singleton instance
config = Config()
