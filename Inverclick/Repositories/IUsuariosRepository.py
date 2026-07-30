from typing import Any
from Models.users import UserDTO

class IUsuariosRepository:
    """
    Interfaz para el repositorio de usuarios.
    """
    def get_by_id(self, user_id: int) -> UserDTO | None:
        """Obtiene un usuario por su ID."""
        pass

    def get_by_email(self, email: str) -> UserDTO | None:
        """Obtiene un usuario por su correo electrónico."""
        pass

    def get_by_identification(self, identification: str, identification_type: str) -> UserDTO | None:
        """Obtiene un usuario por su número de identificación y tipo."""
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        """Obtiene una lista paginada de todos los usuarios."""
        pass

    def create(self, userDTO: UserDTO) -> UserDTO:
        """Crea y persiste un nuevo usuario en la base de datos."""
        pass

    def update(self, user_id: int, userDTO: UserDTO | dict[str, Any]) -> UserDTO | None:
        """Actualiza los datos de un usuario existente."""
        pass

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        pass