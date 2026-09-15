from Repositories.ISaleRepository import ISaleRepository
from Repositories.ILeadRepository import ILeadRepository
from Repositories.IPropertyPlaceholderRepository import IPropertyPlaceholderRepository
from Models.sale import SaleDTO
from Models.property_placeholder import PropertyStatus
from Utils.HttpResponses.saleHttpResponses import SaleHttpResponses


class SaleService:
    def __init__(
        self,
        repository: ISaleRepository,
        lead_repository: ILeadRepository,
        property_repository: IPropertyPlaceholderRepository,
        http_responses: SaleHttpResponses,
    ):
        self.repository = repository
        self.lead_repository = lead_repository
        self.property_repository = property_repository
        self.http_responses = http_responses

    def get_by_id(self, sale_id: int) -> SaleDTO:
        sale = self.repository.get_by_id(sale_id)
        if sale is None:
            raise self.http_responses.error_sale_not_found()
        return sale

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        return self.repository.get_all(skip, limit)

    def create(self, sale_data: SaleDTO) -> SaleDTO:
        """
        Registra una venta, validando las reglas de negocio del CA3 antes
        de guardar nada:
          1. El lead indicado debe existir (trazabilidad).
          2. La propiedad indicada debe existir.
          3. La propiedad NO debe estar ya vendida (evita ventas dobles).
          4. La propiedad SÍ debe estar listada en el catálogo disponible.
        """
        lead = self.lead_repository.get_by_id(sale_data.lead_id)
        if lead is None:
            raise self.http_responses.error_lead_not_found()

        property_ = self.property_repository.get_by_id(
            sale_data.property_id)
        if property_ is None:
            raise self.http_responses.error_property_not_found()

        if property_.status == PropertyStatus.SOLD:
            raise self.http_responses.error_property_already_sold()

        if property_.status != PropertyStatus.LISTED:
            raise self.http_responses.error_property_not_listed()

        sale = self.repository.create(sale_data)

        # Una vez vendida, se bloquea para que nadie más pueda venderla.
        self.property_repository.mark_as_sold(property_.id)

        return sale
