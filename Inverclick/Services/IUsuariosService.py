from typing import Any
from Models.users import UserDTO
from Services.Impl.UsuariosService import UsuariosService

class IUsuariosService:
    """
    Interfaz para el servicio de usuarios.
    """
    def get_by_id(self, user_id: int) -> UserDTO | None:
        """Obtiene un usuario por su ID."""
        UsuariosService.get_by_id(user_id)
        pass

    def get_by_email(self, email: str) -> UserDTO | None:
        """Obtiene un usuario por su correo electrónico."""
        UsuariosService.get_by_email(email)
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        """Obtiene una lista paginada de todos los usuarios."""
        UsuariosService.get_all(skip, limit)
        pass

    def create(self, userDTO: UserDTO) -> UserDTO:
        """Crea y persiste un nuevo usuario en la base de datos."""
        UsuariosService.create(userDTO)
        pass

    def update(self, user_id: int, userDTO: UserDTO) -> UserDTO | None:
        """Actualiza los datos de un usuario existente."""
        UsuariosService.update(userDTO, user_id)
        pass

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        UsuariosService.delete(user_id)
        pass
