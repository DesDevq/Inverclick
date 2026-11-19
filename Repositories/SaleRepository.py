from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.sale import SaleDTO


class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sale_id: int) -> SaleDTO | None:
        statement = select(SaleDTO).where(SaleDTO.id == sale_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SaleDTO]:
        statement = select(SaleDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def get_by_property_id(self, property_id: int) -> SaleDTO | None:
        """Usado para la regla de negocio: ¿esta propiedad ya se vendió?"""
        statement = select(SaleDTO).where(
            SaleDTO.property_id == property_id)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, sale: SaleDTO) -> SaleDTO:
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale
