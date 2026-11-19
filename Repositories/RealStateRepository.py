from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.real_state import RealStateDTO


class RealStateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, real_state_id: int) -> RealStateDTO | None:
        """Obtiene una propiedad por su ID."""
        statement = select(RealStateDTO).where(
            RealStateDTO.id == real_state_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_name(self, name: str) -> RealStateDTO | None:
        """Obtiene una propiedad por su nombre (debe ser único)."""
        statement = select(RealStateDTO).where(RealStateDTO.name == name)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_address(self, address: str) -> RealStateDTO | None:
        """Obtiene una propiedad por su dirección exacta (debe ser única)."""
        statement = select(RealStateDTO).where(RealStateDTO.address == address)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RealStateDTO]:
        """Obtiene una lista paginada de todas las propiedades."""
        statement = select(RealStateDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_constructora(self, constructora_id: int, skip: int = 0, limit: int = 100) -> list[RealStateDTO]:
        """Obtiene solo las propiedades que pertenecen a una constructora específica."""
        statement = select(RealStateDTO).where(
            RealStateDTO.constructora_id == constructora_id).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, real_stateDTO: RealStateDTO) -> RealStateDTO:
        """Crea y persiste una nueva propiedad en la base de datos."""
        self.db.add(real_stateDTO)
        self.db.commit()
        self.db.refresh(real_stateDTO)
        return real_stateDTO

    def update(self, real_state_id: int, real_stateDTO: RealStateDTO | dict[str, Any]) -> RealStateDTO | None:
        """Actualiza los datos de una propiedad existente."""
        db_real_state = self.get_by_id(real_state_id)
        if db_real_state:
            data = real_stateDTO if isinstance(real_stateDTO, dict) else {
                k: v for k, v in real_stateDTO.__dict__.items() if not k.startswith('_')}
            for key, value in data.items():
                if value is not None and hasattr(db_real_state, key):
                    setattr(db_real_state, key, value)
            self.db.commit()
            self.db.refresh(db_real_state)
        return db_real_state

    def delete(self, real_state_id: int) -> bool:
        """Elimina una propiedad por su ID."""
        db_real_state = self.get_by_id(real_state_id)
        if db_real_state:
            self.db.delete(db_real_state)
            self.db.commit()
            return True
        return False
