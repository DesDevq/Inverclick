from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.log import LogDTO


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log: LogDTO) -> LogDTO:
        """Guarda un nuevo registro de auditoría en la base de datos."""
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LogDTO]:
        """Obtiene los logs más recientes primero, de forma paginada."""
        statement = (
            select(LogDTO)
            .order_by(LogDTO.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(statement).scalars().all())
