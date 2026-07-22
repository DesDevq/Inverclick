from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.users import Usuario

class UsuariosRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        """Obtiene un usuario por su ID utilizando la sintaxis de SQLAlchemy 2.0."""
        statement = select(Usuario).where(Usuario.id == usuario_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> Usuario | None:
        """Obtiene un usuario por su correo electrónico."""
        statement = select(Usuario).where(Usuario.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """Obtiene una lista paginada de todos los usuarios."""
        statement = select(Usuario).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, nombre: str, email: str) -> Usuario:
        """Crea y persiste un nuevo usuario en la base de datos."""
        db_usuario = Usuario(nombre=nombre, email=email)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def update(self, usuario_id: int, nombre: str = None, email: str = None) -> Usuario | None:
        """Actualiza los datos de un usuario existente."""
        db_usuario = self.get_by_id(usuario_id)
        if db_usuario:
            if nombre is not None:
                db_usuario.nombre = nombre
            if email is not None:
                db_usuario.email = email
            self.db.commit()
            self.db.refresh(db_usuario)
        return db_usuario

    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        db_usuario = self.get_by_id(usuario_id)
        if db_usuario:
            self.db.delete(db_usuario)
            self.db.commit()
            return True
        return False
