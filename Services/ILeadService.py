from typing import Any
from Models.lead import LeadDTO
from Services.Impl.LeadService import LeadService


class ILeadService:
    """Interfaz para el servicio de leads."""

    def get_by_id(self, lead_id: int) -> LeadDTO:
        return LeadService.get_by_id(self, lead_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return LeadService.get_all(self, skip, limit)

    def create(self, lead: LeadDTO) -> LeadDTO:
        return LeadService.create(self, lead)

    def update(self, lead_id: int, lead_data: dict[str, Any]) -> LeadDTO:
        return LeadService.update(self, lead_id, lead_data)
