from typing import Any
from Models.users_login import UserLoginDTO
from Services.Impl.UsersLoginService import UsersLoginService

class IUsersLoginService:
    """
    Interfaz para el servicio de login de usuarios.
    """
    def get_by_id(self, login_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por su ID."""
        return UsersLoginService.get_by_id(self, login_id)

    def get_by_user_id(self, user_id: int) -> UserLoginDTO | None:
        """Obtiene un registro de login por el ID de usuario."""
        return UsersLoginService.get_by_user_id(self, user_id)

    def get_by_user_login(self, user_login: str) -> UserLoginDTO | None:
        """Obtiene un registro de login por su nombre de login."""
        return UsersLoginService.get_by_user_login(self, user_login)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserLoginDTO]:
        """Obtiene una lista paginada de todos los registros de login."""
        return UsersLoginService.get_all(self, skip, limit)

    def create(self, loginDTO: UserLoginDTO) -> UserLoginDTO:
        """Crea y persiste un nuevo registro de login en la base de datos."""
        return UsersLoginService.create(self, loginDTO)

    def update(self, login_id: int, loginDTO: UserLoginDTO | dict[str, Any]) -> UserLoginDTO | None:
        """Actualiza los datos de un registro de login existente."""
        return UsersLoginService.update(self, login_id, loginDTO)

    def delete(self, login_id: int) -> bool:
        """Elimina un registro de login por su ID."""
        return UsersLoginService.delete(self, login_id)

    def verify_credentials(self, user_login: str, plain_password: str) -> UserLoginDTO | None:
        """Verifica las credenciales de un usuario de login."""
        return UsersLoginService.verify_credentials(self, user_login, plain_password)

    def authenticate(self, user_login: str, plain_password: str) -> UserLoginDTO:
        """Autentica a un usuario y maneja excepciones en caso de error."""
        return UsersLoginService.authenticate(self, user_login, plain_password)
