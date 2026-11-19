# log.py
# CA4: Modelo para el historial de auditoría (logs informáticos).
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base


class LogDTO(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, Identity(
        always=False, start=1), primary_key=True)
    # Usuario que ejecutó la acción. Puede ser None si la petición no traía
    # un token válido (por ejemplo, un intento fallido de login).
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    http_method: Mapped[str] = mapped_column(String(10), nullable=False)
    route: Mapped[str] = mapped_column(String(255), nullable=False)
    status_code: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)
    action_summary: Mapped[str] = mapped_column(String(255), nullable=False)
    # Guarda fecha y hora en una sola columna (timestamp).
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow)


# --- Esquema Pydantic para exponer los logs por API (solo lectura) ---


class LogResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    http_method: str
    route: str
    status_code: Optional[int] = None
    action_summary: str
    created_at: datetime
