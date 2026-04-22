"""
Configuration loading for the Ollama-backed agent.

No API key required — Ollama runs locally on your machine, typically at
http://localhost:11434. That's why this file is simpler than the Anthropic
version: we only need the model name and base URL.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env into os.environ if present. Safe no-op if missing.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable config snapshot."""
    model: str
    base_url: str
    temperature: float = 0.0


def load_settings() -> Settings:
    """Read env vars and return a Settings object."""
    return Settings(
        model=os.getenv("AGENT_MODEL", "llama3.1:8b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )
