from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.constructora import ConstructoraDTO

# el repositorio se comunica con la base de datos


class ConstructoraRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, constructora_id: int) -> ConstructoraDTO | None:
        """Obtiene una constructora por su ID."""
        statement = select(ConstructoraDTO).where(
            ConstructoraDTO.id == constructora_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_nit(self, nit: str) -> ConstructoraDTO | None:
        """Obtiene una constructora por su NIT."""
        statement = select(ConstructoraDTO).where(ConstructoraDTO.nit == nit)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ConstructoraDTO]:
        """Obtiene una lista paginada de todas las constructoras."""
        statement = select(ConstructoraDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, constructoraDTO: ConstructoraDTO) -> ConstructoraDTO:
        """Crea y persiste una nueva constructora en la base de datos."""
        self.db.add(constructoraDTO)
        self.db.commit()
        self.db.refresh(constructoraDTO)
        return constructoraDTO

    def update(self, constructora_id: int, constructoraDTO: ConstructoraDTO | dict[str, Any]) -> ConstructoraDTO | None:
        """Actualiza los datos de una constructora existente."""
        db_constructora = self.get_by_id(constructora_id)
        if db_constructora:
            data = constructoraDTO if isinstance(constructoraDTO, dict) else {
                k: v for k, v in constructoraDTO.__dict__.items() if not k.startswith('_')}
            for key, value in data.items():
                if value is not None and hasattr(db_constructora, key):
                    setattr(db_constructora, key, value)
            self.db.commit()
            self.db.refresh(db_constructora)
        return db_constructora

    def delete(self, constructora_id: int) -> bool:
        """Elimina una constructora por su ID."""
        db_constructora = self.get_by_id(constructora_id)
        if db_constructora:
            self.db.delete(db_constructora)
            self.db.commit()
            return True
        return False
