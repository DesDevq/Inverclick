#!/usr/bin/env python3
"""Indexa los PDFs de data/rag_pdfs en Supabase con pgvector.

Uso:
    .venv/bin/python scripts/rag_ingest.py
    .venv/bin/python scripts/rag_ingest.py --reset
"""

#convierte todos los pdfs en chunks de texto, genera embeddings y los guarda en la base de datos supabase

from _future_ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

from openai import OpenAI
from pypdf import PdfReader

PROJECT_ROOT = Path(_file_).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Models.rag import RagChunkDTO  # noqa: E402
from Repositories.RagRepository import RagRepository  # noqa: E402
from Repositories.database import SessionLocal  # noqa: E402
from Utils.rag_config import settings  # noqa: E402

PDF_ROOT = PROJECT_ROOT / "data" / "rag_pdfs"
MANIFEST_PATH = PDF_ROOT / "manifest.json"
BATCH_SIZE = 32


def clean_pdf_text(text: str) -> str:
    text = text.replace("\x00", " ")
    # Quitar encabezado/pie que ReportLab repite en cada página.
    text = re.sub(r"Inverclick\s*-\s*Documentos RAG\s*Página\s*\d+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"Página\s*\d+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"Proyecto ID:\s*[0-9a-f-]{36}", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            window = text[start:end]
            cut = max(
                window.rfind(". "),
                window.rfind("? "),
                window.rfind("! "),
                window.rfind("; "),
            )
            if cut >= int(size * 0.55):
                end = start + cut + 1

        chunk = text[start:end].strip()
        if len(chunk) >= 60:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)

    return chunks


def load_manifest() -> dict[str, dict]:
    if not MANIFEST_PATH.exists():
        return {}
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {doc["file"]: doc for doc in data.get("documents", [])}


def embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []
    total = len(texts)
    for start in range(0, total, BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=batch,
        )
        batch_vectors = [item.embedding for item in response.data]
        if len(batch_vectors) != len(batch):
            raise RuntimeError("El modelo devolvió una cantidad inesperada de embeddings.")
        for vector in batch_vectors:
            if len(vector) != settings.embedding_dimensions:
                raise RuntimeError(
                    f"Embedding de {len(vector)} dimensiones; se esperaban "
                    f"{settings.embedding_dimensions}."
                )
        vectors.extend(batch_vectors)
        print(f"    embeddings {min(start + BATCH_SIZE, total)}/{total}", flush=True)
    return vectors


def iter_pdfs() -> list[Path]:
    if not PDF_ROOT.exists():
        raise FileNotFoundError(
            f"No existe {PDF_ROOT}. Ejecuta primero scripts/rag_build_pdfs.py"
        )
    return sorted(PDF_ROOT.glob(".pdf")) + sorted((PDF_ROOT / "proyectos").glob(".pdf"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Indexa PDFs en Supabase con pgvector.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Borra todos los chunks antes de reindexar.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    pdfs = iter_pdfs()
    if not pdfs:
        raise SystemExit("No hay PDFs para indexar.")

    embedding_client = OpenAI(
        api_key=settings.embedding_api_key,
        base_url=settings.embedding_base_url,
        timeout=120.0,
    )

    db = SessionLocal()
    repository = RagRepository(db)
    started = time.time()
    total_chunks = 0

    try:
        if args.reset:
            print("Borrando chunks existentes...")
            repository.delete_all()

        for index, pdf_path in enumerate(pdfs, start=1):
            relative = str(pdf_path.relative_to(PDF_ROOT))
            meta = manifest.get(relative, {})
            title = meta.get("title") or pdf_path.stem
            print(f"\n[{index}/{len(pdfs)}] {relative} -> {title}")

            reader = PdfReader(str(pdf_path))
            chunks: list[RagChunkDTO] = []
            chunk_index = 0

            for page_number, page in enumerate(reader.pages, start=1):
                # La página 1 es la portada del PDF; no aporta al RAG.
                if page_number == 1:
                    continue
                page_text = clean_pdf_text(page.extract_text() or "")
                if not page_text:
                    continue
                for piece in chunk_text(page_text, settings.chunk_size, settings.chunk_overlap):
                    chunks.append(
                        RagChunkDTO(
                            source=relative,
                            title=title,
                            page=page_number,
                            chunk_index=chunk_index,
                            content=piece,
                            embedding=[],
                            chunk_metadata={
                                "category": meta.get("category", "general"),
                                "source_url": (meta.get("sources") or [None])[0],
                                "project_id": meta.get("project_id"),
                            },
                        )
                    )
                    chunk_index += 1

            if not chunks:
                print("    sin texto extraíble, se omite.")
                continue

            print(f"    {len(chunks)} chunks; generando embeddings...")
            vectors = embed_texts(embedding_client, [chunk.content for chunk in chunks])
            for chunk, vector in zip(chunks, vectors, strict=True):
                chunk.embedding = vector

            repository.replace_source(relative, chunks)
            total_chunks += len(chunks)
            print(f"    guardado en Supabase ({len(chunks)} chunks).")

        elapsed = time.time() - started
        print("\n========================================")
        print(f"PDFs indexados: {len(pdfs)}")
        print(f"Chunks totales: {total_chunks}")
        print(f"Tiempo: {elapsed:.1f} s")
        print(f"Chunks en la tabla: {repository.count()}")
        print("========================================")
    finally:
        db.close()


if _name_ == "_main_":
    main()