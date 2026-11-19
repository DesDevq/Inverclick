from Services.Impl.prefixService import PrefixService
from Models.prefix import Prefix

class IPrefixService:

    def get_by_id(self, prefix_id: int) -> Prefix | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        pass
