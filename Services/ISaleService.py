from Models.sale import SaleDTO
from Services.Impl.SaleService import SaleService


class ISaleService:
    """Interfaz para el servicio de ventas."""

    def get_by_id(self, sale_id: int) -> SaleDTO:
        return SaleService.get_by_id(self, sale_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        return SaleService.get_all(self, skip, limit)

    def create(self, sale_data: SaleDTO) -> SaleDTO:
        return SaleService.create(self, sale_data)
