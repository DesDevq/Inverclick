from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.IUsersLoginService import IUsersLoginService
from Repositories.UsersLoginRepository import UsersLoginRepository
from Repositories.UsuariosRepository import UsersRepository
from Services.Impl.UsersLoginService import UsersLoginService
from Utils.HttpResponses.userLoginHttpResponses import UserLoginHttpResponses
from Utils.user_login_validator import UserLoginValidator
from Repositories.database import get_db
from Services.Security.JWTHandler import create_access_token
from Repositories.UsersRoleRepository import UsersRoleRepository
from Services.Security.AuthMiddleware import require_module, security

from Models.users_login import (
    UserLoginDTO,
    LoginRequestSchema,
    UserLoginCreateSchema,
    UserLoginUpdateSchema,
    UserLoginResponseSchema,
    TokenResponseSchema
)

# los endpoints solo pueden ser modificados con el role que tenga como modulo "users-login"

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/users-login", tags=["UsersLogin"])

# Dependencia para resolver e instanciar el servicio de login de usuarios


def get_users_login_service(db: Session = Depends(get_db)) -> IUsersLoginService:
    repository = UsersLoginRepository(db)
    users_repository = UsersRepository(db)
    roles_repository = UsersRoleRepository(db)
    http_responses = UserLoginHttpResponses()
    validator = UserLoginValidator()
    return UsersLoginService(repository, http_responses, validator, users_repository, roles_repository)

# --- Endpoints del API ---


# Sin protección: nadie tiene token todavía al momento de loguearse
@router.post("/login", response_model=TokenResponseSchema)
def login(credentials: LoginRequestSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    login_data, role_name, constructora_id = service.authenticate(
        credentials.user_login, credentials.user_password)

    token_data = {
        "sub": str(login_data.user_id),
        "user_login": login_data.user_login,
        "role": role_name
    }

    # Solo se agrega constructora_id al token si el usuario realmente tiene una asignada
    if constructora_id is not None:
        token_data["constructora_id"] = constructora_id

    access_token = create_access_token(token_data)

    return TokenResponseSchema(access_token=access_token)


# Protege este endpoint: solo lo puede usar un token cuyo rol tenga el módulo "users-login" habilitado
@router.get("/{login_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("users-login"))])
def get_login_by_id(login_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_id(login_id)


@router.get("/user/{user_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("users-login"))])
def get_login_by_user_id(user_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_user_id(user_id)


@router.get("/login/{user_login}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("users-login"))])
def get_login_by_user_login(user_login: str, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_by_user_login(user_login)


@router.get("", response_model=list[UserLoginResponseSchema], dependencies=[Depends(require_module("users-login"))])
def get_all_logins(skip: int = 0, limit: int = 100, service: IUsersLoginService = Depends(get_users_login_service)):
    return service.get_all(skip=skip, limit=limit)


@router.post("", status_code=201, response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("users-login"))])
def create_login(login: UserLoginCreateSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    login_dto = UserLoginDTO(**login.model_dump(exclude_none=True))
    return service.create(login_dto)


@router.put("/{login_id}", response_model=UserLoginResponseSchema, dependencies=[Depends(require_module("users-login"))])
def update_login(login_id: int, login: UserLoginUpdateSchema, service: IUsersLoginService = Depends(get_users_login_service)):
    login_dto = UserLoginDTO(**login.model_dump(exclude_unset=True))
    return service.update(login_id, login_dto)


@router.delete("/{login_id}", dependencies=[Depends(require_module("users-login"))])
def delete_login(login_id: int, service: IUsersLoginService = Depends(get_users_login_service)):
    return {"success": service.delete(login_id)}
