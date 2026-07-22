from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Prefix(Base):
    __tablename__ = "prefix"

    id: Mapped[int] = mapped_column(primary_key=True)
    pais: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    codigo: Mapped[str] = mapped_column(String(100))
