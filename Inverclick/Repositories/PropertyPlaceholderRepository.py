from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.property_placeholder import PropertyPlaceholderDTO, PropertyStatus


class PropertyPlaceholderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, property_id: int) -> PropertyPlaceholderDTO | None:
        statement = select(PropertyPlaceholderDTO).where(
            PropertyPlaceholderDTO.id == property_id)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, property_dto: PropertyPlaceholderDTO) -> PropertyPlaceholderDTO:
        self.db.add(property_dto)
        self.db.commit()
        self.db.refresh(property_dto)
        return property_dto

    def mark_as_sold(self, property_id: int) -> None:
        """Marca la propiedad como vendida para bloquear futuras ventas."""
        property_dto = self.get_by_id(property_id)
        if property_dto is not None:
            property_dto.status = PropertyStatus.SOLD
            self.db.commit()
