from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Services.ILogService import ILogService
from Repositories.LogRepository import LogRepository
from Services.Impl.LogService import LogService
from Repositories.database import get_db
from Models.log import LogResponseSchema
from Services.Security.AuthMiddleware import require_module, security


# --- Configuración de Rutas con APIRouter ---
router = APIRouter(prefix="/logs", tags=["Logs"])


def get_log_service(db: Session = Depends(get_db)) -> ILogService:
    repository = LogRepository(db)
    return LogService(repository)


# --- Endpoints del API ---

# Solo lectura: consulta el historial de auditoría (CA4).
# Protegido: solo un rol con el módulo "logs" habilitado puede verlo.
@router.get("", response_model=list[LogResponseSchema], dependencies=[Depends(require_module("logs"))])
def get_all_logs(skip: int = 0, limit: int = 100, service: ILogService = Depends(get_log_service)):
    return service.get_all(skip=skip, limit=limit)
