from Models.users import Usuario
from sqlalchemy.orm import Session

class IUsuariosRepository:
    """
    Interfaz para el repositorio de usuarios.
    """
    def get_by_id(self, usuario_id: int) -> Usuario | None:
        """Obtiene un usuario por su ID."""
        pass

    def get_by_email(self, email: str) -> Usuario | None:
        """Obtiene un usuario por su correo electrónico."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """Obtiene una lista paginada de todos los usuarios."""
        pass

    def create(self, nombre: str, email: str) -> Usuario:
        """Crea y persiste un nuevo usuario en la base de datos."""
        pass

    def update(self, usuario_id: int, nombre: str = None, email: str = None) -> Usuario | None:
        """Actualiza los datos de un usuario existente."""
        pass

    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario por su ID."""
        pass