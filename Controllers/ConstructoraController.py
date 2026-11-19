from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.Impl.ConstructoraService import ConstructoraService
from Repositories.ConstructoraRepository import ConstructoraRepository
from Repositories.PrefixRepository import PrefixRepository
from Utils.HttpResponses.constructoraHttpResponses import ConstructoraHttpResponses
from Utils.constructora_validator import ConstructoraValidator
from Repositories.database import get_db
from Models.constructora import ConstructoraDTO, ConstructoraCreateSchema, ConstructoraUpdateSchema, ConstructoraResponseSchema
from Services.Security.AuthMiddleware import require_module, get_current_user_context

router = APIRouter(prefix="/constructoras", tags=["Constructoras"])


def get_constructora_service(db: Session = Depends(get_db)) -> ConstructoraService:
    repository = ConstructoraRepository(db)
    prefix_repository = PrefixRepository(db)
    http_responses = ConstructoraHttpResponses()
    validator = ConstructoraValidator()
    return ConstructoraService(repository, prefix_repository, http_responses, validator)


@router.get("/{constructora_id}", response_model=ConstructoraResponseSchema, dependencies=[Depends(require_module("constructora"))])
def get_constructora_by_id(
    constructora_id: int,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    return service.get_by_id(constructora_id, current_user)


@router.get("/nit/{nit}", response_model=ConstructoraResponseSchema, dependencies=[Depends(require_module("constructora"))])
def get_constructora_by_nit(
    nit: str,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    return service.get_by_nit(nit, current_user)


@router.get("", response_model=list[ConstructoraResponseSchema], dependencies=[Depends(require_module("constructora"))])
def get_all_constructoras(
    skip: int = 0, limit: int = 100,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    return service.get_all(current_user, skip=skip, limit=limit)


@router.post("", status_code=201, response_model=ConstructoraResponseSchema, dependencies=[Depends(require_module("constructora"))])
def create_constructora(
    constructora: ConstructoraCreateSchema,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    constructora_dto = ConstructoraDTO(
        **constructora.model_dump(exclude_none=True))
    return service.create(constructora_dto, current_user)


@router.put("/{constructora_id}", response_model=ConstructoraResponseSchema, dependencies=[Depends(require_module("constructora"))])
def update_constructora(
    constructora_id: int, constructora: ConstructoraUpdateSchema,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    constructora_dto = ConstructoraDTO(
        **constructora.model_dump(exclude_unset=True))
    return service.update(constructora_id, constructora_dto, current_user)


@router.delete("/{constructora_id}", dependencies=[Depends(require_module("constructora"))])
def delete_constructora(
    constructora_id: int,
    service: ConstructoraService = Depends(get_constructora_service),
    current_user: dict = Depends(get_current_user_context)
):
    return {"success": service.delete(constructora_id, current_user)}
