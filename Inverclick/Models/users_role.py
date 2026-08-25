# users_role.py
from typing import Optional
from sqlalchemy import String, Integer, Identity, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class UserRoleDTO(Base):
    __tablename__ = "users_role"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    modules: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True, default=list)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class UserRoleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    role: str
    modules: Optional[list[str]] = []

class UserRoleUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    role: Optional[str] = None
    modules: Optional[list[str]] = None

class UserRoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    modules: Optional[list[str]] = []
