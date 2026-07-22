from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.users import Usuario
from Services.IUsuariosService import IUsuariosService
from Services.Impl.UsuariosService import UsuariosService
from Repositories.UsuariosRepository import UsuariosRepository
from Repositories.database import get_db

# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Dependencia para resolver e instanciar la interfaz IUsuariosService
def get_usuarios_service(db: Session = Depends(get_db)) -> IUsuariosService:
    repository = UsuariosRepository(db)
    return UsuariosService(repository)

# --- Endpoints del API ---

@router.get("/{usuario_id}")
def get_user_by_id(usuario_id: int, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return service.get_by_id(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/email/{email}")
def get_user_by_email(email: str, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return service.get_by_email(email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("")
def get_all_users(skip: int = 0, limit: int = 100, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return service.get_all(skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("", status_code=201)
def create_user(nombre: str, email: str, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return service.create(nombre=nombre, email=email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}")
def update_user(usuario_id: int, nombre: str = None, email: str = None, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return service.update(usuario_id=usuario_id, nombre=nombre, email=email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}")
def delete_user(usuario_id: int, service: IUsuariosService = Depends(get_usuarios_service)):
    try:
        return {"success": service.delete(usuario_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))