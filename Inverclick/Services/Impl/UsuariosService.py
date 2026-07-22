from Repositories.IUsuariosRepository import IUsuariosRepository
from Models.users import Usuario
from Repositories.PrefixRepository import PrefixRepository

class UsuariosService:
    def __init__(self, repository: IUsuariosRepository, prefixRepository: PrefixRepository):
        self.repository = repository

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        user: Usuario | None = self.repository.get_by_id(usuario_id)
        if user is None:
            raise ValueError("Usuario no encontrado")
        return user

    def get_by_email(self, email: str) -> Usuario | None:
        user: Usuario | None = self.repository.get_by_email(email)
        if user is None:
            raise ValueError("Usuario no encontrado")
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        users: list[Usuario] = self.repository.get_all(skip, limit)
        if users is None:
            raise ValueError("Usuarios no encontrados")
        return users

    def create(self, nombre: str, email: str) -> Usuario:

        if self.repository.get_by_email(email) is not None:
            raise ValueError("El email ya existe")

        prefix = self.prefixRepository.get_by_prefix("+58")
        if prefix is None:
            raise ValueError("Prefijo no encontrado")

        user: Usuario = self.repository.create(nombre, email)
        if user is None:
            raise ValueError("Usuario no creado")
        return user

    def update(self, usuario_id: int, nombre: str = None, email: str = None) -> Usuario | None:
        user: Usuario | None = self.repository.update(usuario_id, nombre, email)
        if user is None:
            raise ValueError("Usuario no actualizado")
        return user

    def delete(self, usuario_id: int) -> bool:
        user: bool = self.repository.delete(usuario_id)
        if user is None:
            raise ValueError("Usuario no eliminado")
        return user
