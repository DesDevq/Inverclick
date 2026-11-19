from typing import Any
from Models.users_role import UserRoleDTO
from Repositories.UsersRoleRepository import UsersRoleRepository

class IUsersRoleRepository:
    """
    Interfaz para el repositorio de roles de usuario.
    """
    def get_by_id(self, role_id: int) -> UserRoleDTO | None:
        """Obtiene un rol por su ID."""
        return UsersRoleRepository.get_by_id(self, role_id)

    def get_by_role(self, role: str) -> UserRoleDTO | None:
        """Obtiene un rol por su nombre."""
        return UsersRoleRepository.get_by_role(self, role)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserRoleDTO]:
        """Obtiene una lista paginada de todos los roles."""
        return UsersRoleRepository.get_all(self, skip, limit)

    def create(self, roleDTO: UserRoleDTO) -> UserRoleDTO:
        """Crea y persiste un nuevo rol en la base de datos."""
        return UsersRoleRepository.create(self, roleDTO)

    def update(self, role_id: int, roleDTO: UserRoleDTO | dict[str, Any]) -> UserRoleDTO | None:
        """Actualiza los datos de un rol existente."""
        return UsersRoleRepository.update(self, role_id, roleDTO)

    def delete(self, role_id: int) -> bool:
        """Elimina un rol por su ID."""
        return UsersRoleRepository.delete(self, role_id)
