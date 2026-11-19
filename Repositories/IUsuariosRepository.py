from typing import Any
from Models.users import UserDTO
from Repositories.UsuariosRepository import UsersRepository

class IUsuariosRepository:
    """
    Interfaz para el repositorio de usuarios.
    """
    def get_by_id(self, user_id: int) -> UserDTO | None:
        """Obtiene un usuario por su ID."""
        UserDTO = UsersRepository.get_by_id(user_id)
        pass

    def get_by_email(self, email: str) -> UserDTO | None:
        """Obtiene un usuario por su correo electrónico."""
        UserDTO = UsersRepository.get_by_email(email)
        pass

    def get_by_identification(self, identification: str, identification_type: str) -> UserDTO | None:
        """Obtiene un usuario por su número de identificación y tipo."""
        UserDTO = UsersRepository.get_by_identification(identification, identification_type)
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO] | None:
        """Obtiene una lista paginada de todos los usuarios."""
        ListDTO = UsersRepository.get_all(skip, limit)
        pass

    def create(self, userDTO: UserDTO) -> UserDTO:
        """Crea y persiste un nuevo usuario en la base de datos."""
        UserDTO = UsersRepository.create(userDTO)
        pass

    def update(self, user_id: int, userDTO: UserDTO | dict[str, Any]) -> UserDTO | None:
        """Actualiza los datos de un usuario existente."""
        UserDTO = UsersRepository.update(userDTO, user_id)
        pass

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        UsersRepository.delete(user_id)
        pass