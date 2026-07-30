from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Prefix(Base):
    __tablename__ = "countries"
    __table_args__ = {"schema": "inverclick"}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str] = mapped_column(String(100), nullable=False)
    country_phone_code: Mapped[str] = mapped_column(String(10), nullable=False)
    
