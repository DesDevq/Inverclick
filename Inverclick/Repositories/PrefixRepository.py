from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.prefix import Prefix

class PrefixRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, Prefix_id: int) -> Prefix | None:
        """Obtiene un Prefix por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(Prefix).where(Prefix.id == Prefix_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        """Obtiene una lista paginada de todos los Prefixs."""
        statement = select(Prefix).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_code(self, code: str) -> Prefix | None:
        """Obtiene un Prefix por su código."""
        statement = select(Prefix).where(Prefix.country_phone_code == code)
        return self.db.execute(statement).scalar_one_or_none()

