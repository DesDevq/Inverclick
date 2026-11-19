from Models.sale import SaleDTO


class ISaleRepository:
    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        pass

    def get_by_property_id(self, property_id: int) -> SaleDTO | None:
        pass

    def create(self, sale: SaleDTO) -> SaleDTO:
        pass
