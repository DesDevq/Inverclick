from Repositories.ISaleRepository import ISaleRepository
from Repositories.ILeadRepository import ILeadRepository
from Repositories.RealStateRepository import RealStateRepository
from Models.sale import SaleDTO
from Utils.HttpResponses.saleHttpResponses import SaleHttpResponses

# Valores de 'status' que usa la tabla real_state (CA2).
AVAILABLE_STATUS = "disponible"
SOLD_STATUS = "vendida"


class SaleService:
    def __init__(
        self,
        repository: ISaleRepository,
        lead_repository: ILeadRepository,
        real_state_repository: RealStateRepository,
        http_responses: SaleHttpResponses,
    ):
        self.repository = repository
        self.lead_repository = lead_repository
        self.real_state_repository = real_state_repository
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
          4. La propiedad SÍ debe estar disponible en el catálogo (CA2).
        """
        lead = self.lead_repository.get_by_id(sale_data.lead_id)
        if lead is None:
            raise self.http_responses.error_lead_not_found()

        real_state = self.real_state_repository.get_by_id(
            sale_data.property_id)
        if real_state is None:
            raise self.http_responses.error_property_not_found()

        if real_state.status == SOLD_STATUS:
            raise self.http_responses.error_property_already_sold()

        if real_state.status != AVAILABLE_STATUS:
            raise self.http_responses.error_property_not_listed()

        sale = self.repository.create(sale_data)

        # Una vez vendida, se bloquea para que nadie más pueda venderla.
        self.real_state_repository.update(
            real_state.id, {"status": SOLD_STATUS})

        return sale
