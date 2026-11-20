"""Configuración del módulo de Gestión Documental.

La carpeta de almacenamiento vive fuera del proyecto (variable UPLOAD_DIR en
.env) para que los archivos subidos nunca queden dentro del código ni del
control de versiones.
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


@dataclass(frozen=True)
class DocumentSettings:
    upload_dir: Path

    @classmethod
    def from_env(cls) -> "DocumentSettings":
        upload_dir = Path(_env("UPLOAD_DIR"))
        upload_dir.mkdir(parents=True, exist_ok=True)
        return cls(upload_dir=upload_dir)


settings = DocumentSettings.from_env()
