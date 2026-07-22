from Repositories.IPrefixRepository import IPrefixRepository
from Models.prefix import Prefix

class PrefixService:
    def __init__(self, repository: IPrefixRepository):
        self.repository = repository

    def get_by_id(self, prefix_id: int) -> Prefix | None:
        prefix: Prefix | None = self.repository.get_by_id(prefix_id)
        if prefix is None:
            raise ValueError("Prefix no encontrado")
        return prefix

    def get_by_prefix(self, prefix: str) -> Prefix | None:
        prefix: Prefix | None = self.repository.get_by_prefix(prefix)
        if prefix is None:
            raise ValueError("Prefijo no encontrado")   
        return prefix

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        prefixes: list[Prefix] = self.repository.get_all(skip, limit)
        if prefixes is None:
            raise ValueError("Prefixs no encontrados")
        return prefixes