"""LocalClaw configuration management"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama2")
    
    # Web UI
    WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT = int(os.getenv("WEB_PORT", 8000))
    WEB_DEBUG = os.getenv("WEB_DEBUG", "False").lower() == "true"
    
    # File reading
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 1048576))  # 1MB
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Singleton instance
config = Config()
