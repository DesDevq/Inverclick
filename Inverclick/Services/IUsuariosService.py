from Services.Impl.UsuariosService import UsuariosService
from Models.users import Usuario

class IUsuariosService:
    """
    Interfaz para el servicio de usuarios.
    """
    def get_by_id(self, usuario_id: int) -> Usuario | None:
        pass

    """Obtiene un usuario por su ID."""
    def get_by_email(self, email: str) -> Usuario | None:
        pass

    """Obtiene un usuario por su correo electrónico."""
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        pass

    """Obtiene una lista paginada de todos los usuarios."""
    def create(self, nombre: str, email: str) -> Usuario:
        pass

    """Crea y persiste un nuevo usuario en la base de datos."""
    def update(self, usuario_id: int, nombre: str = None, email: str = None) -> Usuario | None:
        pass

    """Actualiza los datos de un usuario existente."""

    def delete(self, usuario_id: int) -> bool:
        pass
