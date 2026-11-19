from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.users_role import UserRoleDTO

class UsersRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, role_id: int) -> UserRoleDTO | None:
        """Obtiene un rol por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(UserRoleDTO).where(UserRoleDTO.id == role_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_role(self, role: str) -> UserRoleDTO | None:
        """Obtiene un rol por su nombre."""
        statement = select(UserRoleDTO).where(UserRoleDTO.role == role)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserRoleDTO]:
        """Obtiene una lista paginada de todos los roles."""
        statement = select(UserRoleDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, roleDTO: UserRoleDTO) -> UserRoleDTO:
        """Crea y persiste un nuevo rol en la base de datos."""
        self.db.add(roleDTO)
        self.db.commit()
        self.db.refresh(roleDTO)
        return roleDTO

    def update(self, role_id: int, roleDTO: UserRoleDTO | dict[str, Any]) -> UserRoleDTO | None:
        """Actualiza los datos de un rol existente."""
        db_role = self.get_by_id(role_id)
        if db_role:
            data = roleDTO if isinstance(roleDTO, dict) else {k: v for k, v in roleDTO.__dict__.items() if not k.startswith('_')}
            for key, value in data.items():
                if value is not None and hasattr(db_role, key):
                    setattr(db_role, key, value)
            self.db.commit()
            self.db.refresh(db_role)
        return db_role

    def delete(self, role_id: int) -> bool:
        """Elimina un rol por su ID."""
        db_role = self.get_by_id(role_id)
        if db_role:
            self.db.delete(db_role)
            self.db.commit()
            return True
        return False
