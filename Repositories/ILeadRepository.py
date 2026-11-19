from Models.lead import LeadDTO


class ILeadRepository:
    def get_by_id(self, lead_id: int) -> LeadDTO | None:
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LeadDTO]:
        pass

    def create(self, lead: LeadDTO) -> LeadDTO:
        pass

    def update(self, lead_id: int, lead_data: dict) -> LeadDTO | None:
        pass
