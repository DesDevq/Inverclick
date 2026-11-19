"""Configuración del módulo RAG.

Todas las variables viven en .env para que el código sea el mismo en local,
en la nube o con otro proveedor de modelos.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Falta la variable {name} en .env. "
            "Revisa .env.example para ver la configuración completa."
        )
    return value.strip()


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


@dataclass(frozen=True)
class RagSettings:
    opencode_api_key: str
    opencode_base_url: str
    llm_model: str
    llm_max_tokens: int
    embedding_base_url: str
    embedding_api_key: str
    embedding_model: str
    embedding_dimensions: int
    top_k: int
    chunk_size: int
    chunk_overlap: int

    @classmethod
    def from_env(cls) -> "RagSettings":
        return cls(
            # Se valida al usar el chat, no al importar el módulo.
            opencode_api_key=os.getenv("OPENCODE_API_KEY", "").strip(),
            opencode_base_url=_env(
                "OPENCODE_BASE_URL",
                "https://opencode.ai/inference/go/openai/v1",
            ),
            llm_model=_env("LLM_MODEL", "deepseek-v4.1-flash"),
            llm_max_tokens=_env_int("LLM_MAX_TOKENS", 2000),
            embedding_base_url=_env("EMBEDDING_BASE_URL", "http://localhost:11434/v1"),
            embedding_api_key=_env("EMBEDDING_API_KEY", "ollama"),
            embedding_model=_env("EMBEDDING_MODEL", "qwen3-embedding:0.6b"),
            embedding_dimensions=_env_int("EMBEDDING_DIMENSIONS", 1024),
            top_k=_env_int("RAG_TOP_K", 10),
            chunk_size=_env_int("RAG_CHUNK_SIZE", 900),
            chunk_overlap=_env_int("RAG_CHUNK_OVERLAP", 150),
        )


settings = RagSettings.from_env()