from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.ISaleService import ISaleService
from Repositories.SaleRepository import SaleRepository
from Repositories.LeadRepository import LeadRepository
from Repositories.RealStateRepository import RealStateRepository
from Services.Impl.SaleService import SaleService
from Utils.HttpResponses.saleHttpResponses import SaleHttpResponses
from Repositories.database import get_db
from Models.sale import SaleDTO, SaleCreateSchema, SaleResponseSchema
from Services.Security.AuthMiddleware import require_module, security

router = APIRouter(prefix="/sales", tags=["Sales"])


def get_sale_service(db: Session = Depends(get_db)) -> ISaleService:
    repository = SaleRepository(db)
    lead_repository = LeadRepository(db)
    real_state_repository = RealStateRepository(db)
    http_responses = SaleHttpResponses()
    return SaleService(repository, lead_repository, real_state_repository, http_responses)


@router.get("/{sale_id}", response_model=SaleResponseSchema, dependencies=[Depends(require_module("sales"))])
def get_sale_by_id(sale_id: int, service: ISaleService = Depends(get_sale_service)):
    return service.get_by_id(sale_id)


@router.get("", response_model=list[SaleResponseSchema], dependencies=[Depends(require_module("sales"))])
def get_all_sales(skip: int = 0, limit: int = 100, service: ISaleService = Depends(get_sale_service)):
    return service.get_all(skip=skip, limit=limit)


# Registrar una venta: aquí se validan las reglas de negocio del CA3
# (propiedad ya vendida / no listada) dentro del servicio.
@router.post("", status_code=201, response_model=SaleResponseSchema, dependencies=[Depends(require_module("sales"))])
def create_sale(sale: SaleCreateSchema, service: ISaleService = Depends(get_sale_service)):
    sale_dto = SaleDTO(**sale.model_dump(exclude_none=True))
    return service.create(sale_dto)
