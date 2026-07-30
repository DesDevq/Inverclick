from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.IUsuariosService import IUsuariosService
from Services.Impl.UsuariosService import UsuariosService
from Repositories.UsersRepository import UsersRepository
from Repositories.PrefixRepository import PrefixRepository
from Utils.HttpResponses.userHttpResponses import UserHttpResponses
from Utils.user_validator import UserValidator
from Repositories.database import get_db
from Models.users import UserDTO, UserCreateSchema, UserUpdateSchema, UserResponseSchema

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/users", tags=["Users"])

# Dependencia para resolver e instanciar el servicio de usuarios
def get_usuarios_service(db: Session = Depends(get_db)) -> IUsuariosService:
    repository = UsersRepository(db)
    prefix_repository = PrefixRepository(db)
    http_responses = UserHttpResponses()
    validator = UserValidator()
    return UsuariosService(repository, prefix_repository, http_responses, validator)

# --- Endpoints del API ---

@router.get("/{usuario_id}", response_model=UserResponseSchema)
def get_user_by_id(usuario_id: int, service: IUsuariosService = Depends(get_usuarios_service)):
    return service.get_by_id(usuario_id)

@router.get("/email/{email}", response_model=UserResponseSchema)
def get_user_by_email(email: str, service: IUsuariosService = Depends(get_usuarios_service)):
    return service.get_by_email(email)

@router.get("", response_model=list[UserResponseSchema])
def get_all_users(skip: int = 0, limit: int = 100, service: IUsuariosService = Depends(get_usuarios_service)):
    return service.get_all(skip=skip, limit=limit)

@router.post("", status_code=201, response_model=UserResponseSchema)
def create_user(user: UserCreateSchema, service: IUsuariosService = Depends(get_usuarios_service)):
    user_dto = UserDTO(**user.model_dump(exclude_none=True))
    return service.create(user_dto)

@router.put("/{usuario_id}", response_model=UserResponseSchema)
def update_user(usuario_id: int, user: UserUpdateSchema, service: IUsuariosService = Depends(get_usuarios_service)):
    user_dto = UserDTO(**user.model_dump(exclude_unset=True))
    return service.update(user_id=usuario_id, userDTO=user_dto)

@router.delete("/{usuario_id}")
def delete_user(usuario_id: int, service: IUsuariosService = Depends(get_usuarios_service)):
    return {"success": service.delete(usuario_id)}