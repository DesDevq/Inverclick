from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.users import UserDTO

class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> UserDTO | None:
        """Obtiene un usuario por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(UserDTO).where(UserDTO.id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> UserDTO | None:
        """Obtiene un usuario por su correo electrónico."""
        statement = select(UserDTO).where(UserDTO.email == email)
        return self.db.execute(statement).scalar_one_or_none()
    
    def get_by_identification(self, identification: str, identification_type: str) -> UserDTO | None:
        """Obtiene un usuario por su número de identificación y tipo."""
        statement = select(UserDTO).where(
            UserDTO.identification == identification, 
            UserDTO.identification_type == identification_type
        )
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        """Obtiene una lista paginada de todos los usuarios."""
        statement = select(UserDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, userDTO: UserDTO) -> UserDTO:
        """Crea y persiste un nuevo usuario en la base de datos."""
        self.db.add(userDTO)
        self.db.commit()
        self.db.refresh(userDTO)
        return userDTO

    def update(self, user_id: int, userDTO: UserDTO | dict[str, Any]) -> UserDTO | None:
        """Actualiza los datos de un usuario existente."""
        db_usuario = self.get_by_id(user_id)
        if db_usuario:
            data = userDTO if isinstance(userDTO, dict) else {k: v for k, v in userDTO.__dict__.items() if not k.startswith('_')}
            for key, value in data.items():
                if value is not None and hasattr(db_usuario, key):
                    setattr(db_usuario, key, value)
            self.db.commit()
            self.db.refresh(db_usuario)
        return db_usuario

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        db_usuario = self.get_by_id(user_id)
        if db_usuario:
            self.db.delete(db_usuario)
            self.db.commit()
            return True
        return False
