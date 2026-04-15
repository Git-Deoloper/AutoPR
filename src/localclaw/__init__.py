"""LocalClaw - A fully local, open-source AI code agent"""

__version__ = "0.1.0"
__author__ = "LocalClaw Contributors"
__description__ = "A fully local, open-source AI code agent with Ollama - no API keys required"

from localclaw.core.codebase import CodebaseReader
from localclaw.llm.ollama_client import OllamaClient

__all__ = ["CodebaseReader", "OllamaClient"]
