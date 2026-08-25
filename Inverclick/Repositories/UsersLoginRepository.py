from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.users_login import UserLoginDTO

class UsersLoginRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(UserLoginDTO).where(UserLoginDTO.id == login_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por el ID de usuario."""
        statement = select(UserLoginDTO).where(UserLoginDTO.user_id == user_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_login(self, user_login: str) -> UserLoginDTO | None:
        """Obtiene un registro de login por el nombre de login."""
        statement = select(UserLoginDTO).where(UserLoginDTO.user_login == user_login)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        """Obtiene una lista paginada de todos los registros de login."""
        statement = select(UserLoginDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        """Crea y persiste un nuevo registro de login en la base de datos."""
        self.db.add(loginDTO)
        self.db.commit()
        self.db.refresh(loginDTO)
        return loginDTO

    def update(self, login_id: int, loginDTO: UserLoginDTO | dict[str, Any]) -> UserLoginDTO | None:
        """Actualiza los datos de un registro de login existente."""
        db_login = self.get_by_id(login_id)
        if db_login:
            data = loginDTO if isinstance(loginDTO, dict) else {k: v for k, v in loginDTO.__dict__.items() if not k.startswith('_')}
            for key, value in data.items():
                if value is not None and hasattr(db_login, key):
                    setattr(db_login, key, value)
            self.db.commit()
            self.db.refresh(db_login)
        return db_login

    def delete(self, login_id: int) -> bool:
        """Elimina un registro de login por su ID."""
        db_login = self.get_by_id(login_id)
        if db_login:
            self.db.delete(db_login)
            self.db.commit()
            return True
        return False
