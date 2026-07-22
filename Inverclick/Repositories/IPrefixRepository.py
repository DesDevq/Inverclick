from sqlalchemy.orm import Session
from Models.prefix import Prefix

class IPrefixRepository:
    def get_by_id(self, prefix_id: int) -> Prefix | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Prefix]:
        pass