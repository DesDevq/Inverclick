from datetime import datetime
from typing import Any, Literal, Optional

from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import BigInteger, DateTime, Identity, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from Repositories.database import Base

EMBEDDING_DIMENSIONS = 1024


class RagChunkDTO(Base):
    __tablename__ = "rag_chunks"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIMENSIONS), nullable=False)
    chunk_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


class RagChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class RagChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=2, max_length=2000)
    history: list[RagChatMessage] = Field(default_factory=list, max_length=12)


class RagSource(BaseModel):
    title: Optional[str] = None
    source: str
    page: Optional[int] = None
    chunk_index: int
    score: float


class RagChatResponse(BaseModel):
    answer: str
    sources: list[RagSource]


class RagHealthResponse(BaseModel):
    status: str
    chunks: int
    embedding_model: str
    embedding_dimensions: int
    llm_model: str