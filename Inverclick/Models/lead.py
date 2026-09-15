# lead.py
# CA3: un Lead es un cliente interesado en una propiedad, antes de que
# se convierta (o no) en una venta.
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class LeadDTO(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    # Usuario interesado (cliente potencial).
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("real_state.id"), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="nuevo")
    description: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---


class LeadCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    user_id: int
    property_id: int
    status: Optional[str] = "nuevo"
    description: Optional[str] = None
    source: Optional[str] = None


class LeadUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    status: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None


class LeadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    property_id: int
    status: str
    description: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[datetime] = None
