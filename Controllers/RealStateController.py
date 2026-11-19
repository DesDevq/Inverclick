from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.Impl.RealStateService import RealStateService
from Repositories.RealStateRepository import RealStateRepository
from Repositories.ConstructoraRepository import ConstructoraRepository
from Repositories.PrefixRepository import PrefixRepository
from Utils.HttpResponses.realStateHttpResponses import RealStateHttpResponses
from Utils.real_state_validator import RealStateValidator
from Repositories.database import get_db
from Models.real_state import RealStateDTO, RealStateCreateSchema, RealStateUpdateSchema, RealStateResponseSchema
from Services.Security.AuthMiddleware import require_module, get_current_user_context

router = APIRouter(prefix="/real-state", tags=["RealState"])


def get_real_state_service(db: Session = Depends(get_db)) -> RealStateService:
    repository = RealStateRepository(db)
    constructora_repository = ConstructoraRepository(db)
    prefix_repository = PrefixRepository(db)
    http_responses = RealStateHttpResponses()
    validator = RealStateValidator()
    return RealStateService(repository, constructora_repository, prefix_repository, http_responses, validator)


@router.get("/{real_state_id}", response_model=RealStateResponseSchema, dependencies=[Depends(require_module("real_state"))])
def get_real_state_by_id(
    real_state_id: int,
    service: RealStateService = Depends(get_real_state_service),
    current_user: dict = Depends(get_current_user_context)
):
    return service.get_by_id(real_state_id, current_user)


@router.get("", response_model=list[RealStateResponseSchema], dependencies=[Depends(require_module("real_state"))])
def get_all_real_states(
    skip: int = 0, limit: int = 100,
    service: RealStateService = Depends(get_real_state_service),
    current_user: dict = Depends(get_current_user_context)
):
    return service.get_all(current_user, skip=skip, limit=limit)


@router.post("", status_code=201, response_model=RealStateResponseSchema, dependencies=[Depends(require_module("real_state"))])
def create_real_state(
    real_state: RealStateCreateSchema,
    service: RealStateService = Depends(get_real_state_service),
    current_user: dict = Depends(get_current_user_context)
):
    real_state_dto = RealStateDTO(**real_state.model_dump(exclude_none=True))
    return service.create(real_state_dto, current_user)


@router.put("/{real_state_id}", response_model=RealStateResponseSchema, dependencies=[Depends(require_module("real_state"))])
def update_real_state(
    real_state_id: int, real_state: RealStateUpdateSchema,
    service: RealStateService = Depends(get_real_state_service),
    current_user: dict = Depends(get_current_user_context)
):
    real_state_dto = RealStateDTO(**real_state.model_dump(exclude_unset=True))
    return service.update(real_state_id, real_state_dto, current_user)


@router.delete("/{real_state_id}", dependencies=[Depends(require_module("real_state"))])
def delete_real_state(
    real_state_id: int,
    service: RealStateService = Depends(get_real_state_service),
    current_user: dict = Depends(get_current_user_context)
):
    return {"success": service.delete(real_state_id, current_user)}
