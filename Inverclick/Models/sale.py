# sale.py
# CA3: una Venta conecta un Lead, el agente que la gestionó, el cliente
# que compró y la propiedad adquirida. Es el registro de trazabilidad
# comercial completo que pide la historia de usuario.
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, DateTime, ForeignKey, Identity, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class SaleDTO(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    # De qué lead vino la conversión (trazabilidad).
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leads.id"), nullable=False)
    # Usuario vendedor (agente de ventas que gestionó la transacción).
    agent_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    # Usuario comprador (cliente final).
    buyer_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    # TODO: cambiar a la tabla real de Propiedades cuando exista (CA2).
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("properties_placeholder.id"), nullable=False)
    sale_price: Mapped[Optional[float]] = mapped_column(
        Numeric, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---


class SaleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    lead_id: int
    agent_user_id: int
    buyer_user_id: int
    property_id: int
    sale_price: Optional[float] = None


class SaleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    agent_user_id: int
    buyer_user_id: int
    property_id: int
    sale_price: Optional[float] = None
    created_at: Optional[datetime] = None
