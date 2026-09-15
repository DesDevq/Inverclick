from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.ILeadService import ILeadService
from Repositories.LeadRepository import LeadRepository
from Services.Impl.LeadService import LeadService
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses
from Repositories.database import get_db
from Models.lead import LeadDTO, LeadCreateSchema, LeadUpdateSchema, LeadResponseSchema
from Services.Security.AuthMiddleware import require_module, security

router = APIRouter(prefix="/leads", tags=["Leads"])


def get_lead_service(db: Session = Depends(get_db)) -> ILeadService:
    repository = LeadRepository(db)
    http_responses = LeadHttpResponses()
    return LeadService(repository, http_responses)


@router.get("/{lead_id}", response_model=LeadResponseSchema, dependencies=[Depends(require_module("leads"))])
def get_lead_by_id(lead_id: int, service: ILeadService = Depends(get_lead_service)):
    return service.get_by_id(lead_id)


@router.get("", response_model=list[LeadResponseSchema], dependencies=[Depends(require_module("leads"))])
def get_all_leads(skip: int = 0, limit: int = 100, service: ILeadService = Depends(get_lead_service)):
    return service.get_all(skip=skip, limit=limit)


@router.post("", status_code=201, response_model=LeadResponseSchema, dependencies=[Depends(require_module("leads"))])
def create_lead(lead: LeadCreateSchema, service: ILeadService = Depends(get_lead_service)):
    lead_dto = LeadDTO(**lead.model_dump(exclude_none=True))
    return service.create(lead_dto)


@router.put("/{lead_id}", response_model=LeadResponseSchema, dependencies=[Depends(require_module("leads"))])
def update_lead(lead_id: int, lead: LeadUpdateSchema, service: ILeadService = Depends(get_lead_service)):
    return service.update(lead_id, lead.model_dump(exclude_unset=True))
