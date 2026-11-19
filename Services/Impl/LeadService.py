from typing import Any
from Repositories.ILeadRepository import ILeadRepository
from Models.lead import LeadDTO
from Utils.HttpResponses.leadHttpResponses import LeadHttpResponses


class LeadService:
    def __init__(self, repository: ILeadRepository, http_responses: LeadHttpResponses):
        self.repository = repository
        self.http_responses = http_responses

    def get_by_id(self, lead_id: int) -> LeadDTO:
        lead = self.repository.get_by_id(lead_id)
        if lead is None:
            raise self.http_responses.error_lead_not_found()
        return lead

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        return self.repository.get_all(skip, limit)

    def create(self, lead: LeadDTO) -> LeadDTO:
        created = self.repository.create(lead)
        if created is None:
            raise self.http_responses.error_lead_not_created()
        return created

    def update(self, lead_id: int, lead_data: dict[str, Any]) -> LeadDTO:
        lead = self.repository.update(lead_id, lead_data)
        if lead is None:
            raise self.http_responses.error_lead_not_updated()
        return lead
