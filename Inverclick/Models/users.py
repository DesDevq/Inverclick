# models.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from Repositories.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    # Tipado estricto con Mapped y mapped_column
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))