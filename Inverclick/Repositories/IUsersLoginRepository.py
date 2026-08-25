from typing import Any
from Models.users_login import UserLoginDTO
from Repositories.UsersLoginRepository import UsersLoginRepository

class IUsersLoginRepository:
    """
    Interfaz para el repositorio de login de usuarios.
    """
    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por su ID."""
        return UsersLoginRepository.get_by_id(self, login_id)

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por el ID de usuario."""
        return UsersLoginRepository.get_by_user_id(self, user_id)

    def get_by_user_login(self, user_login: str) -> UserLoginDTO | None:
        """Obtiene un registro de login por el nombre de login."""
        return UsersLoginRepository.get_by_user_login(self, user_login)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        """Obtiene una lista paginada de todos los registros de login."""
        return UsersLoginRepository.get_all(self, skip, limit)

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        """Crea y persiste un nuevo registro de login en la base de datos."""
        return UsersLoginRepository.create(self, loginDTO)

    def update(self, login_id: int, loginDTO: UserLoginDTO | dict[str, Any]) -> UserLoginDTO | None:
        """Actualiza los datos de un registro de login existente."""
        return UsersLoginRepository.update(self, login_id, loginDTO)

    def delete(self, login_id: int) -> bool:
        """Elimina un registro de login por su ID."""
        return UsersLoginRepository.delete(self, login_id)
