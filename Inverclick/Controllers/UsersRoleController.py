from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.IUsersRoleService import IUsersRoleService
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Impl.UsersRoleService import UsersRoleService
from Utils.HttpResponses.userRoleHttpResponses import UserRoleHttpResponses
from Utils.user_role_validator import UserRoleValidator
from Repositories.database import get_db
from Models.users_role import UserRoleDTO, UserRoleCreateSchema, UserRoleUpdateSchema, UserRoleResponseSchema
from Services.Security.AuthMiddleware import require_module, security


# los endpoints solo pueden ser modificados con el role que tenga como modulo "users-role"

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/users-role", tags=["UsersRole"])

# Dependencia para resolver e instanciar el servicio de roles de usuario


def get_users_role_service(db: Session = Depends(get_db)) -> IUsersRoleService:
    repository = UsersRoleRepository(db)
    http_responses = UserRoleHttpResponses()
    validator = UserRoleValidator()
    return UsersRoleService(repository, http_responses, validator)

# --- Endpoints del API ---

# Protege este endpoint: solo lo puede usar un token cuyo rol tenga el módulo "users-role" habilitado


@router.get("/{role_id}", response_model=UserRoleResponseSchema, dependencies=[Depends(require_module("users-role"))])
def get_role_by_id(role_id: int, service: IUsersRoleService = Depends(get_users_role_service)):
    return service.get_by_id(role_id)


@router.get("/name/{role_name}", response_model=UserRoleResponseSchema, dependencies=[Depends(require_module("users-role"))])
def get_role_by_name(role_name: str, service: IUsersRoleService = Depends(get_users_role_service)):
    return service.get_by_role(role_name)


@router.get("", response_model=list[UserRoleResponseSchema], dependencies=[Depends(require_module("users-role"))])
def get_all_roles(skip: int = 0, limit: int = 100, service: IUsersRoleService = Depends(get_users_role_service)):
    return service.get_all(skip=skip, limit=limit)


@router.post("", status_code=201, response_model=UserRoleResponseSchema, dependencies=[Depends(require_module("users-role"))])
def create_role(role: UserRoleCreateSchema, service: IUsersRoleService = Depends(get_users_role_service)):
    role_dto = UserRoleDTO(**role.model_dump(exclude_none=True))
    return service.create(role_dto)


@router.put("/{role_id}", response_model=UserRoleResponseSchema, dependencies=[Depends(require_module("users-role"))])
def update_role(role_id: int, role: UserRoleUpdateSchema, service: IUsersRoleService = Depends(get_users_role_service)):
    role_dto = UserRoleDTO(**role.model_dump(exclude_unset=True))
    return service.update(role_id, role_dto)


@router.delete("/{role_id}", dependencies=[Depends(require_module("users-role"))])
def delete_role(role_id: int, service: IUsersRoleService = Depends(get_users_role_service)):
    return {"success": service.delete(role_id)}
