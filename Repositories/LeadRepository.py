from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from Models.lead import LeadDTO


class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        statement = select(LeadDTO).where(LeadDTO.id == lead_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        statement = select(LeadDTO).offset(skip).limit(limit)
        return list(self.db.execute(statement).scalars().all())

    def create(self, lead: LeadDTO) -> LeadDTO:
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def update(self, lead_id: int, lead_data: dict[str, Any]) -> LeadDTO | None:
        lead = self.get_by_id(lead_id)
        if lead is None:
            return None
        for field, value in lead_data.items():
            setattr(lead, field, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead
