# models.py
from datetime import datetime, date
from typing import Optional, Union
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, Identity, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from Repositories.database import Base
from Utils.enums import IdentificationTypeEnum

class UserDTO(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(Integer, Identity(always=False, start=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    identification: Mapped[str] = mapped_column(String(100), nullable=False)
    identification_type: Mapped[IdentificationTypeEnum] = mapped_column(
        SQLEnum(IdentificationTypeEnum, native_enum=False, length=3), 
        nullable=False
    )
    country_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("inverclick.countries.id"), nullable=True)
    user_id_role: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("inverclick.users_role.id"), nullable=True)
    residence_city: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    street_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    job: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    monthly_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    monthly_outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    desired_description: Mapped[str] = mapped_column(String(500), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.utcnow)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

# --- Esquemas Pydantic con validación estricta (extra='forbid') ---

class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str
    last_name: str
    email: Optional[str] = None
    identification: str
    identification_type: str
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    desired_description: str
    date_of_birth: Optional[date] = None

class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    identification: Optional[str] = None
    identification_type: Optional[str] = None
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    desired_description: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    email: Optional[str] = None
    identification: str
    identification_type: str
    country_id: Optional[int] = None
    user_id_role: Optional[int] = None
    residence_city: Optional[str] = None
    street_address: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    job: Optional[str] = None
    monthly_income: Optional[str] = None
    monthly_outcome: Optional[str] = None
    desired_description: str
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    date_of_birth: Optional[Union[date, datetime]] = None
