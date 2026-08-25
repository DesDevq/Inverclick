# users_login.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base

class UserLoginDTO(Base):
    __tablename__ = "users_login"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("inverclick.users.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_login: Mapped[str] = mapped_column(String(100), nullable=False)
    user_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class LoginRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    user_login: str
    user_password: str

class UserLoginCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    user_id: int
    user_login: str
    user_password: Optional[str] = None
    active: Optional[bool] = True

class UserLoginUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    user_login: Optional[str] = None
    user_password: Optional[str] = None
    active: Optional[bool] = None

class UserLoginResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    user_login: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    active: Optional[bool] = True
