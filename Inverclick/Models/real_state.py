# real_state.py
from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Numeric, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class RealStateDTO(Base):
    __tablename__ = "real_state"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True)
    value: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    constructora_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("constructora.id"), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("countries.id"), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="disponible")
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---


class RealStateCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str
    address: str
    value: Decimal
    constructora_id: int
    description: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    status: Optional[str] = "disponible"


class RealStateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: Optional[str] = None
    address: Optional[str] = None
    value: Optional[Decimal] = None
    constructora_id: Optional[int] = None
    description: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    status: Optional[str] = None


class RealStateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    value: Decimal
    constructora_id: int
    description: Optional[str] = None
    city: Optional[str] = None
    country_id: Optional[int] = None
    status: str
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
