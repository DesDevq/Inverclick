# constructora.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class ConstructoraDTO(Base):
    __tablename__ = "constructora"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    nit: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("countries.id"), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---


class ConstructoraCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str
    nit: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None


class ConstructoraUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: Optional[str] = None
    nit: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None


class ConstructoraResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    nit: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
