# PropertyPlaceholderController.py
#
# ATENCION: controlador TEMPORAL solo para poder crear propiedades de
# prueba mientras no existe la tabla real de Propiedades (CA2). Bórralo
# cuando tu compañera termine su parte y uses su controlador real.
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Repositories.PropertyPlaceholderRepository import PropertyPlaceholderRepository
from Repositories.database import get_db
from Models.property_placeholder import PropertyPlaceholderDTO, PropertyStatus
from Services.Security.AuthMiddleware import require_module, security

router = APIRouter(prefix="/properties-placeholder", tags=["Properties (temporal)"])


class PropertyPlaceholderCreateSchema(BaseModel):
    name: str
    status: str = PropertyStatus.LISTED


@router.post("", status_code=201, dependencies=[Depends(require_module("properties-placeholder"))])
def create_property_placeholder(
    property_in: PropertyPlaceholderCreateSchema,
    db: Session = Depends(get_db),
):
    repository = PropertyPlaceholderRepository(db)
    property_dto = PropertyPlaceholderDTO(**property_in.model_dump())
    return repository.create(property_dto)


@router.get("/{property_id}", dependencies=[Depends(require_module("properties-placeholder"))])
def get_property_placeholder(property_id: int, db: Session = Depends(get_db)):
    repository = PropertyPlaceholderRepository(db)
    return repository.get_by_id(property_id)
